"""
Crop Suitability Matcher

Matches predicted climate conditions with a comprehensive crop database to
compute multi-factor suitability scores.  The database covers 30+ crops
commonly grown in South/South-East Asia.
"""
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Comprehensive crop database (30+ crops)
# Each crop defines:
#   temp_range      – ideal growing temperature range (°C)
#   rainfall_range  – ideal annual rainfall range (mm / year average monthly × 12 ≈ ×12)
#   rainfall_monthly_range – average monthly rainfall range (mm)
#   ph_range        – tolerable soil-pH range
#   nitrogen_need   – "low" | "medium" | "high"
#   drought_tolerance  – 0-1 score
#   heat_tolerance     – 0-1 score
#   flood_tolerance    – 0-1 score
#   soil_types      – acceptable soil classifications
#   planting_season – recommended sowing window
#   expected_yield  – typical yield (kg/ha)
#   description     – brief human-readable summary
# ---------------------------------------------------------------------------
CROP_DATABASE: Dict[str, Dict] = {
    "Millet": {
        "temp_range": (20, 38),
        "rainfall_monthly_range": (30, 100),
        "ph_range": (5.5, 7.5),
        "nitrogen_need": "low",
        "drought_tolerance": 0.95,
        "heat_tolerance": 0.92,
        "flood_tolerance": 0.30,
        "soil_types": ["Sandy", "Loamy", "Red"],
        "planting_season": "June–July",
        "expected_yield": 1900,
        "description": "Highly drought and heat-tolerant cereal grain.",
    },
    "Sorghum": {
        "temp_range": (18, 40),
        "rainfall_monthly_range": (25, 90),
        "ph_range": (5.5, 8.0),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.92,
        "heat_tolerance": 0.90,
        "flood_tolerance": 0.35,
        "soil_types": ["Alluvial", "Loamy", "Black"],
        "planting_season": "June–July",
        "expected_yield": 2200,
        "description": "Versatile drought-resistant cereal suitable for semi-arid regions.",
    },
    "Pigeon Pea": {
        "temp_range": (18, 38),
        "rainfall_monthly_range": (50, 120),
        "ph_range": (5.0, 7.5),
        "nitrogen_need": "low",
        "drought_tolerance": 0.88,
        "heat_tolerance": 0.85,
        "flood_tolerance": 0.25,
        "soil_types": ["Sandy", "Loamy", "Red"],
        "planting_season": "June–July",
        "expected_yield": 1600,
        "description": "Nitrogen-fixing legume; ideal companion in dry rotations.",
    },
    "Cowpea": {
        "temp_range": (18, 40),
        "rainfall_monthly_range": (30, 100),
        "ph_range": (5.5, 8.0),
        "nitrogen_need": "low",
        "drought_tolerance": 0.90,
        "heat_tolerance": 0.88,
        "flood_tolerance": 0.30,
        "soil_types": ["Sandy", "Loamy"],
        "planting_season": "June–August",
        "expected_yield": 1200,
        "description": "Fast-maturing legume with high drought endurance.",
    },
    "Groundnut": {
        "temp_range": (20, 35),
        "rainfall_monthly_range": (60, 130),
        "ph_range": (5.5, 7.0),
        "nitrogen_need": "low",
        "drought_tolerance": 0.75,
        "heat_tolerance": 0.80,
        "flood_tolerance": 0.20,
        "soil_types": ["Sandy", "Loamy", "Red"],
        "planting_season": "June–July",
        "expected_yield": 2500,
        "description": "Important oilseed crop tolerant to moderate drought.",
    },
    "Sesame": {
        "temp_range": (25, 40),
        "rainfall_monthly_range": (20, 80),
        "ph_range": (5.5, 8.0),
        "nitrogen_need": "low",
        "drought_tolerance": 0.88,
        "heat_tolerance": 0.90,
        "flood_tolerance": 0.15,
        "soil_types": ["Sandy", "Loamy", "Red"],
        "planting_season": "July–August",
        "expected_yield": 800,
        "description": "High-value oilseed well-adapted to hot, dry climates.",
    },
    "Maize": {
        "temp_range": (18, 35),
        "rainfall_monthly_range": (80, 200),
        "ph_range": (5.5, 7.5),
        "nitrogen_need": "high",
        "drought_tolerance": 0.50,
        "heat_tolerance": 0.65,
        "flood_tolerance": 0.30,
        "soil_types": ["Loamy", "Sandy", "Alluvial"],
        "planting_season": "June–July",
        "expected_yield": 5000,
        "description": "High-yield cereal requiring moderate to good water supply.",
    },
    "Rice": {
        "temp_range": (20, 35),
        "rainfall_monthly_range": (100, 250),
        "ph_range": (5.0, 7.0),
        "nitrogen_need": "high",
        "drought_tolerance": 0.20,
        "heat_tolerance": 0.55,
        "flood_tolerance": 0.95,
        "soil_types": ["Alluvial", "Clay", "Loamy"],
        "planting_season": "June–July (Kharif)",
        "expected_yield": 4500,
        "description": "Staple cereal; water-intensive and flood-tolerant.",
    },
    "Wheat": {
        "temp_range": (10, 25),
        "rainfall_monthly_range": (40, 120),
        "ph_range": (6.0, 7.5),
        "nitrogen_need": "high",
        "drought_tolerance": 0.40,
        "heat_tolerance": 0.35,
        "flood_tolerance": 0.25,
        "soil_types": ["Alluvial", "Loamy", "Clay"],
        "planting_season": "November–December (Rabi)",
        "expected_yield": 4000,
        "description": "Major Rabi cereal; performs best in cool, moist winters.",
    },
    "Barley": {
        "temp_range": (8, 24),
        "rainfall_monthly_range": (30, 100),
        "ph_range": (6.0, 8.0),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.55,
        "heat_tolerance": 0.40,
        "flood_tolerance": 0.25,
        "soil_types": ["Alluvial", "Loamy", "Sandy"],
        "planting_season": "October–November",
        "expected_yield": 3000,
        "description": "Hardy cereal tolerant of mild drought and cool conditions.",
    },
    "Chickpea": {
        "temp_range": (10, 30),
        "rainfall_monthly_range": (30, 100),
        "ph_range": (6.0, 8.0),
        "nitrogen_need": "low",
        "drought_tolerance": 0.70,
        "heat_tolerance": 0.45,
        "flood_tolerance": 0.20,
        "soil_types": ["Alluvial", "Loamy", "Red"],
        "planting_season": "October–November",
        "expected_yield": 1800,
        "description": "Nitrogen-fixing Rabi pulse; moderate drought tolerance.",
    },
    "Lentil": {
        "temp_range": (10, 25),
        "rainfall_monthly_range": (30, 90),
        "ph_range": (6.0, 8.0),
        "nitrogen_need": "low",
        "drought_tolerance": 0.65,
        "heat_tolerance": 0.35,
        "flood_tolerance": 0.20,
        "soil_types": ["Alluvial", "Loamy"],
        "planting_season": "October–December",
        "expected_yield": 1200,
        "description": "High-protein Rabi pulse; tolerates mild drought.",
    },
    "Mustard": {
        "temp_range": (10, 25),
        "rainfall_monthly_range": (30, 90),
        "ph_range": (5.5, 7.5),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.60,
        "heat_tolerance": 0.40,
        "flood_tolerance": 0.20,
        "soil_types": ["Alluvial", "Loamy"],
        "planting_season": "October–November",
        "expected_yield": 1500,
        "description": "Important oilseed Rabi crop; survives light frost.",
    },
    "Sunflower": {
        "temp_range": (18, 35),
        "rainfall_monthly_range": (50, 150),
        "ph_range": (6.0, 7.5),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.65,
        "heat_tolerance": 0.75,
        "flood_tolerance": 0.30,
        "soil_types": ["Alluvial", "Loamy", "Black"],
        "planting_season": "February–March / June–July",
        "expected_yield": 2000,
        "description": "Versatile oilseed crop grown in both Kharif and Rabi seasons.",
    },
    "Cotton": {
        "temp_range": (20, 38),
        "rainfall_monthly_range": (50, 130),
        "ph_range": (5.5, 8.0),
        "nitrogen_need": "high",
        "drought_tolerance": 0.55,
        "heat_tolerance": 0.75,
        "flood_tolerance": 0.20,
        "soil_types": ["Black/Regur", "Alluvial", "Loamy"],
        "planting_season": "April–June",
        "expected_yield": 1800,
        "description": "Major fibre crop; prefers hot weather and well-drained soils.",
    },
    "Sugarcane": {
        "temp_range": (20, 38),
        "rainfall_monthly_range": (100, 250),
        "ph_range": (6.0, 7.5),
        "nitrogen_need": "high",
        "drought_tolerance": 0.30,
        "heat_tolerance": 0.65,
        "flood_tolerance": 0.55,
        "soil_types": ["Alluvial", "Loamy", "Clay"],
        "planting_season": "February–March / October",
        "expected_yield": 70000,
        "description": "High-value tropical crop; demands ample water and warmth.",
    },
    "Cassava": {
        "temp_range": (18, 38),
        "rainfall_monthly_range": (50, 150),
        "ph_range": (5.0, 7.5),
        "nitrogen_need": "low",
        "drought_tolerance": 0.88,
        "heat_tolerance": 0.85,
        "flood_tolerance": 0.25,
        "soil_types": ["Sandy", "Loamy"],
        "planting_season": "April–June",
        "expected_yield": 18000,
        "description": "Drought-hardy tropical root crop with high carbohydrate yield.",
    },
    "Sweet Potato": {
        "temp_range": (18, 34),
        "rainfall_monthly_range": (60, 150),
        "ph_range": (5.5, 7.0),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.70,
        "heat_tolerance": 0.75,
        "flood_tolerance": 0.30,
        "soil_types": ["Sandy", "Loamy"],
        "planting_season": "March–April",
        "expected_yield": 12000,
        "description": "Nutrient-rich root vegetable tolerant of moderate drought.",
    },
    "Potato": {
        "temp_range": (10, 25),
        "rainfall_monthly_range": (60, 150),
        "ph_range": (4.8, 7.0),
        "nitrogen_need": "high",
        "drought_tolerance": 0.30,
        "heat_tolerance": 0.25,
        "flood_tolerance": 0.20,
        "soil_types": ["Loamy", "Sandy", "Alluvial"],
        "planting_season": "October–November",
        "expected_yield": 22000,
        "description": "Cool-season tuber with high yield under irrigation.",
    },
    "Tomato": {
        "temp_range": (15, 30),
        "rainfall_monthly_range": (60, 130),
        "ph_range": (5.5, 7.5),
        "nitrogen_need": "high",
        "drought_tolerance": 0.35,
        "heat_tolerance": 0.50,
        "flood_tolerance": 0.20,
        "soil_types": ["Loamy", "Sandy"],
        "planting_season": "October–November / February–March",
        "expected_yield": 25000,
        "description": "High-value vegetable requiring moderate temperatures.",
    },
    "Onion": {
        "temp_range": (10, 30),
        "rainfall_monthly_range": (40, 100),
        "ph_range": (5.5, 7.0),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.55,
        "heat_tolerance": 0.55,
        "flood_tolerance": 0.20,
        "soil_types": ["Alluvial", "Loamy"],
        "planting_season": "October–November / May–June",
        "expected_yield": 20000,
        "description": "Widely cultivated bulb vegetable adaptable to many climates.",
    },
    "Garlic": {
        "temp_range": (10, 25),
        "rainfall_monthly_range": (40, 100),
        "ph_range": (6.0, 7.5),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.50,
        "heat_tolerance": 0.40,
        "flood_tolerance": 0.20,
        "soil_types": ["Alluvial", "Loamy"],
        "planting_season": "October–November",
        "expected_yield": 8000,
        "description": "High-value spice crop thriving in cool-to-mild winters.",
    },
    "Turmeric": {
        "temp_range": (20, 35),
        "rainfall_monthly_range": (100, 250),
        "ph_range": (4.5, 7.5),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.45,
        "heat_tolerance": 0.75,
        "flood_tolerance": 0.40,
        "soil_types": ["Loamy", "Alluvial", "Red"],
        "planting_season": "April–May",
        "expected_yield": 15000,
        "description": "High-value spice rhizome; prefers warm, humid conditions.",
    },
    "Ginger": {
        "temp_range": (20, 30),
        "rainfall_monthly_range": (120, 250),
        "ph_range": (5.5, 6.5),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.30,
        "heat_tolerance": 0.65,
        "flood_tolerance": 0.30,
        "soil_types": ["Loamy", "Sandy", "Red"],
        "planting_season": "April–May",
        "expected_yield": 12000,
        "description": "Aromatic rhizome crop thriving in warm, moist tropics.",
    },
    "Banana": {
        "temp_range": (20, 38),
        "rainfall_monthly_range": (100, 250),
        "ph_range": (5.5, 7.0),
        "nitrogen_need": "high",
        "drought_tolerance": 0.30,
        "heat_tolerance": 0.70,
        "flood_tolerance": 0.45,
        "soil_types": ["Alluvial", "Loamy"],
        "planting_season": "Year-round",
        "expected_yield": 40000,
        "description": "Tropical fruit crop with high yield in humid climates.",
    },
    "Mango": {
        "temp_range": (20, 40),
        "rainfall_monthly_range": (50, 150),
        "ph_range": (5.5, 7.5),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.70,
        "heat_tolerance": 0.85,
        "flood_tolerance": 0.35,
        "soil_types": ["Alluvial", "Loamy", "Red"],
        "planting_season": "Year-round (fruit June–August)",
        "expected_yield": 10000,
        "description": "Popular tropical fruit tree; survives seasonal dry spells.",
    },
    "Papaya": {
        "temp_range": (20, 38),
        "rainfall_monthly_range": (80, 200),
        "ph_range": (5.5, 7.0),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.50,
        "heat_tolerance": 0.80,
        "flood_tolerance": 0.20,
        "soil_types": ["Loamy", "Sandy"],
        "planting_season": "Year-round",
        "expected_yield": 35000,
        "description": "Fast-maturing tropical fruit tree with very high yields.",
    },
    "Green Gram (Moong)": {
        "temp_range": (25, 40),
        "rainfall_monthly_range": (30, 90),
        "ph_range": (6.0, 7.5),
        "nitrogen_need": "low",
        "drought_tolerance": 0.72,
        "heat_tolerance": 0.80,
        "flood_tolerance": 0.20,
        "soil_types": ["Sandy", "Loamy", "Alluvial"],
        "planting_season": "March–April / June–July",
        "expected_yield": 900,
        "description": "Short-duration heat-tolerant summer pulse.",
    },
    "Black Gram (Urad)": {
        "temp_range": (25, 40),
        "rainfall_monthly_range": (30, 100),
        "ph_range": (5.5, 7.5),
        "nitrogen_need": "low",
        "drought_tolerance": 0.70,
        "heat_tolerance": 0.78,
        "flood_tolerance": 0.20,
        "soil_types": ["Loamy", "Alluvial", "Red"],
        "planting_season": "June–July / November–December",
        "expected_yield": 1000,
        "description": "Protein-rich legume adapted to warm and semi-arid conditions.",
    },
    "Amaranth": {
        "temp_range": (18, 38),
        "rainfall_monthly_range": (25, 80),
        "ph_range": (5.5, 8.0),
        "nitrogen_need": "low",
        "drought_tolerance": 0.90,
        "heat_tolerance": 0.88,
        "flood_tolerance": 0.25,
        "soil_types": ["Sandy", "Loamy", "Red"],
        "planting_season": "June–August",
        "expected_yield": 1500,
        "description": "Climate-resilient pseudo-cereal; excellent for arid/semi-arid areas.",
    },
    "Teff": {
        "temp_range": (10, 32),
        "rainfall_monthly_range": (30, 90),
        "ph_range": (5.0, 8.0),
        "nitrogen_need": "low",
        "drought_tolerance": 0.85,
        "heat_tolerance": 0.70,
        "flood_tolerance": 0.45,
        "soil_types": ["Sandy", "Loamy", "Red"],
        "planting_season": "June–July",
        "expected_yield": 1400,
        "description": "Super-grain with extremely high stress tolerance.",
    },
    "Quinoa": {
        "temp_range": (8, 28),
        "rainfall_monthly_range": (20, 80),
        "ph_range": (6.0, 8.5),
        "nitrogen_need": "low",
        "drought_tolerance": 0.80,
        "heat_tolerance": 0.55,
        "flood_tolerance": 0.30,
        "soil_types": ["Sandy", "Loamy"],
        "planting_season": "October–November",
        "expected_yield": 2000,
        "description": "High-protein pseudo-cereal tolerant of drought, frost, and salinity.",
    },
    "Hemp (Industrial)": {
        "temp_range": (15, 30),
        "rainfall_monthly_range": (50, 120),
        "ph_range": (6.0, 7.5),
        "nitrogen_need": "medium",
        "drought_tolerance": 0.65,
        "heat_tolerance": 0.55,
        "flood_tolerance": 0.25,
        "soil_types": ["Loamy", "Alluvial"],
        "planting_season": "March–May",
        "expected_yield": 3000,
        "description": "Multi-purpose fibre/seed crop; improves soil health.",
    },
}


class CropSuitabilityMatcher:
    """Match projected climate conditions with crop suitability requirements."""

    def __init__(self) -> None:
        """Initialise the matcher with the built-in crop database."""
        self.crop_db = CROP_DATABASE

    def compute_suitability_score(
        self,
        crop_name: str,
        projected_temp: float,
        projected_rainfall_monthly: float,
        soil_ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
    ) -> Dict:
        """Compute a 0–1 suitability score for a single crop.

        The overall score is a weighted average of four factor scores:
          - Temperature fit   (35%)
          - Rainfall fit      (30%)
          - Soil pH fit       (20%)
          - Resilience bonus  (15%) based on drought/heat tolerance

        Args:
            crop_name: Key in CROP_DATABASE.
            projected_temp: Projected average temperature (°C).
            projected_rainfall_monthly: Projected average monthly rainfall (mm).
            soil_ph: Soil pH.
            nitrogen: Nitrogen content (kg/ha).
            phosphorus: Phosphorus content (kg/ha).
            potassium: Potassium content (kg/ha).

        Returns:
            Dict with 'score' and component breakdown.
        """
        crop = self.crop_db.get(crop_name)
        if crop is None:
            return {"score": 0.0, "reason": "Crop not found in database."}

        # ── Temperature score ──────────────────────────────────────────
        temp_min, temp_max = crop["temp_range"]
        temp_score = self._range_score(projected_temp, temp_min, temp_max, tolerance=3)

        # ── Rainfall score ─────────────────────────────────────────────
        rain_min, rain_max = crop["rainfall_monthly_range"]
        rain_score = self._range_score(projected_rainfall_monthly, rain_min, rain_max, tolerance=20)

        # ── Soil pH score ──────────────────────────────────────────────
        ph_min, ph_max = crop["ph_range"]
        ph_score = self._range_score(soil_ph, ph_min, ph_max, tolerance=0.5)

        # ── Nutrient fit score ─────────────────────────────────────────
        nitrogen_need = crop["nitrogen_need"]
        nutrient_score = self._nutrient_score(nitrogen_need, nitrogen, phosphorus, potassium)

        # ── Climate resilience bonus ───────────────────────────────────
        # Reward crops that can cope with future stress (drought / heat)
        drought_factor = crop["drought_tolerance"]
        heat_factor = crop["heat_tolerance"]
        resilience_score = 0.5 * drought_factor + 0.5 * heat_factor

        # ── Weighted composite ─────────────────────────────────────────
        overall = (
            0.35 * temp_score
            + 0.30 * rain_score
            + 0.20 * ph_score
            + 0.05 * nutrient_score
            + 0.10 * resilience_score
        )
        overall = round(min(max(overall, 0.0), 1.0), 4)

        return {
            "score": overall,
            "temperature_score": round(temp_score, 4),
            "rainfall_score": round(rain_score, 4),
            "ph_score": round(ph_score, 4),
            "nutrient_score": round(nutrient_score, 4),
            "resilience_score": round(resilience_score, 4),
        }

    def get_top_crops(
        self,
        projected_temp: float,
        projected_rainfall_monthly: float,
        soil_ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        top_n: int = 5,
        min_score: float = 0.30,
    ) -> List[Dict]:
        """Return the top-N most suitable crops for the projected conditions.

        Args:
            projected_temp: Projected mean temperature (°C).
            projected_rainfall_monthly: Projected mean monthly rainfall (mm).
            soil_ph: Soil pH.
            nitrogen: Soil nitrogen (kg/ha).
            phosphorus: Soil phosphorus (kg/ha).
            potassium: Soil potassium (kg/ha).
            top_n: Number of crops to return (default 5).
            min_score: Minimum overall score threshold (default 0.30).

        Returns:
            List of dicts ordered by descending suitability score, each
            containing crop metadata, scores, and planting info.
        """
        results: List[Tuple[float, str, Dict]] = []

        for crop_name, crop_data in self.crop_db.items():
            scores = self.compute_suitability_score(
                crop_name,
                projected_temp,
                projected_rainfall_monthly,
                soil_ph,
                nitrogen,
                phosphorus,
                potassium,
            )
            if scores["score"] >= min_score:
                results.append((scores["score"], crop_name, {**crop_data, **scores}))

        # Sort descending by score
        results.sort(key=lambda x: x[0], reverse=True)

        top_crops = []
        for score, name, data in results[:top_n]:
            top_crops.append(
                {
                    "crop": name,
                    "resilience_score": score,
                    "planting_season": data.get("planting_season", "N/A"),
                    "expected_yield": data.get("expected_yield", 0),
                    "description": data.get("description", ""),
                    "temperature_score": data.get("temperature_score", 0),
                    "rainfall_score": data.get("rainfall_score", 0),
                    "ph_score": data.get("ph_score", 0),
                    "resilience_component": data.get("resilience_score", 0),
                    "drought_tolerance": data.get("drought_tolerance", 0),
                    "heat_tolerance": data.get("heat_tolerance", 0),
                }
            )

        return top_crops

    def get_crop_adaptability(
        self,
        crop_name: str,
        current_temp: float,
        current_rainfall_monthly: float,
        future_temp: float,
        future_rainfall_monthly: float,
        soil_ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
    ) -> Dict:
        """Assess how a specific crop's suitability changes under climate change.

        Args:
            crop_name: Name of the crop.
            current_temp: Current average temperature (°C).
            current_rainfall_monthly: Current average monthly rainfall (mm).
            future_temp: Projected future temperature (°C).
            future_rainfall_monthly: Projected future monthly rainfall (mm).
            soil_ph: Soil pH.
            nitrogen: Soil nitrogen (kg/ha).
            phosphorus: Soil phosphorus (kg/ha).
            potassium: Soil potassium (kg/ha).

        Returns:
            Dict with current score, future score, and change assessment.
        """
        current = self.compute_suitability_score(
            crop_name, current_temp, current_rainfall_monthly,
            soil_ph, nitrogen, phosphorus, potassium,
        )
        future = self.compute_suitability_score(
            crop_name, future_temp, future_rainfall_monthly,
            soil_ph, nitrogen, phosphorus, potassium,
        )

        delta = future["score"] - current["score"]
        if delta > 0.05:
            trend = "improving"
        elif delta < -0.05:
            trend = "declining"
        else:
            trend = "stable"

        return {
            "crop": crop_name,
            "current_suitability": current["score"],
            "future_suitability": future["score"],
            "suitability_change": round(delta, 4),
            "adaptability_trend": trend,
            "is_climate_resilient": future["score"] >= 0.65,
            "details": {
                "current": current,
                "future": future,
            },
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _range_score(value: float, low: float, high: float, tolerance: float = 0) -> float:
        """Compute a smooth 0–1 score for a value within [low, high].

        - 1.0 inside the optimal range.
        - Linearly decreases to 0 outside range within ±tolerance.
        - 0.0 beyond tolerance.
        """
        if low <= value <= high:
            return 1.0
        if value < low:
            gap = low - value
        else:
            gap = value - high
        if tolerance <= 0 or gap > tolerance:
            return 0.0
        return 1.0 - (gap / tolerance)

    @staticmethod
    def _nutrient_score(
        nitrogen_need: str, nitrogen: float, phosphorus: float, potassium: float
    ) -> float:
        """Score nutrient availability relative to crop demand."""
        # Normalised thresholds (kg/ha)
        thresholds = {"low": 40, "medium": 60, "high": 80}
        required = thresholds.get(nitrogen_need, 60)

        n_score = min(nitrogen / required, 1.0) if required > 0 else 1.0
        p_score = min(phosphorus / 40, 1.0)
        k_score = min(potassium / 80, 1.0)

        return (n_score + p_score + k_score) / 3
