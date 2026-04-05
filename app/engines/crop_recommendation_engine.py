"""
Crop Recommendation Engine

Main orchestrator that combines climate data loading, climate prediction,
and crop suitability matching to produce climate-resilient crop recommendations
for a given farm location and soil profile.
"""
import logging
from typing import Dict, List, Optional

from app.engines.climate_data_loader import ClimateDataLoader
from app.engines.climate_prediction_model import ClimatePredictionModel
from app.engines.crop_suitability_matcher import CropSuitabilityMatcher

logger = logging.getLogger(__name__)


class CropRecommendationEngine:
    """Orchestrate the climate-resilient crop recommendation pipeline.

    Pipeline:
    1. Load 30-year historical climate data for the location.
    2. Fit the ensemble ML model on historical data.
    3. Predict future climate (5-10 year horizon).
    4. Merge ML predictions with IPCC delta adjustments.
    5. Rank crops by multi-factor suitability against projected climate.
    6. Generate a human-readable explanation.
    """

    def __init__(self) -> None:
        """Initialise sub-components."""
        self.data_loader = ClimateDataLoader()
        self.prediction_model = ClimatePredictionModel()
        self.suitability_matcher = CropSuitabilityMatcher()

    def recommend(
        self,
        latitude: float,
        longitude: float,
        soil_ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        target_year: int = 2035,
        top_n: int = 5,
    ) -> Dict:
        """Generate climate-resilient crop recommendations.

        Args:
            latitude: Farm latitude (decimal degrees).
            longitude: Farm longitude (decimal degrees).
            soil_ph: Soil pH (4–9).
            nitrogen: Soil nitrogen content (kg/ha).
            phosphorus: Soil phosphorus content (kg/ha).
            potassium: Soil potassium content (kg/ha).
            target_year: Future year for climate projection (default 2035).
            top_n: Number of top crops to return (default 5).

        Returns:
            Dict with recommended_crops, future_climate_summary, and explanation.
        """
        logger.info("Generating recommendations | year=%d", target_year)

        # ── Step 1: Load historical climate data ────────────────────────
        historical = self.data_loader.load_historical_climate_data(latitude, longitude)

        # ── Step 2: Fit ensemble model on historical data ────────────────
        self.prediction_model.fit(
            historical["temperature_monthly"],
            historical["rainfall_monthly"],
        )

        # ── Step 3: IPCC delta projections ───────────────────────────────
        projected_climate = self.data_loader.get_projected_climate(
            latitude, longitude, target_year=target_year
        )

        # ── Step 4: ML-based future projections ──────────────────────────
        n_months_ahead = (target_year - 2024) * 12
        ml_prediction = self.prediction_model.predict_future_climate(
            historical["temperature_monthly"],
            historical["rainfall_monthly"],
            n_months_ahead=max(n_months_ahead, 12),
        )

        # Blend IPCC delta with ML prediction (equal weight)
        # Note: projected_climate["projected_rainfall"] and ml_prediction["predicted_rainfall_avg"]
        # are both monthly averages (mm/month), so no further division is needed.
        final_temp = 0.5 * projected_climate["projected_temp"] + 0.5 * ml_prediction["predicted_temp_avg"]
        final_rainfall_monthly = (
            0.5 * projected_climate["projected_rainfall"]
            + 0.5 * ml_prediction["predicted_rainfall_avg"]
        )

        # ── Step 5: Get top crops ────────────────────────────────────────
        top_crops = self.suitability_matcher.get_top_crops(
            projected_temp=final_temp,
            projected_rainfall_monthly=final_rainfall_monthly,
            soil_ph=soil_ph,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            top_n=top_n,
        )

        # ── Step 6: Climate summary ──────────────────────────────────────
        temp_change = projected_climate["temperature_change"]
        rainfall_pct_change = projected_climate["rainfall_change"]
        climate_zone = projected_climate["climate_zone"]
        confidence = projected_climate["confidence"]

        # Estimate growing-season length change (approx +5 days per +0.5 °C)
        growing_season_change_days = int(temp_change * 10)

        future_climate_summary = {
            "temperature_change": f"+{temp_change:.1f}°C",
            "rainfall_variation": f"{rainfall_pct_change:+.0f}%",
            "growing_season_change": f"+{growing_season_change_days} days",
            "climate_zone": climate_zone,
            "confidence_score": confidence,
            "projected_temp": round(final_temp, 1),
            "projected_rainfall_monthly": round(final_rainfall_monthly, 1),
        }

        # ── Step 7: Human-readable explanation ──────────────────────────
        explanation = self._build_explanation(
            top_crops, temp_change, rainfall_pct_change, climate_zone
        )

        # ── Build climate trend series for visualisation ─────────────────
        trend_series = self._build_trend_series(
            historical, ml_prediction, projected_climate, target_year
        )

        return {
            "recommended_crops": top_crops,
            "future_climate_summary": future_climate_summary,
            "explanation": explanation,
            "climate_trends": trend_series,
        }

    def check_crop_adaptability(
        self,
        crop_name: str,
        latitude: float,
        longitude: float,
        soil_ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        target_year: int = 2035,
    ) -> Dict:
        """Check how well a specific crop will adapt to future climate.

        Args:
            crop_name: Name of the crop to assess.
            latitude: Farm latitude.
            longitude: Farm longitude.
            soil_ph: Soil pH.
            nitrogen: Soil nitrogen (kg/ha).
            phosphorus: Soil phosphorus (kg/ha).
            potassium: Soil potassium (kg/ha).
            target_year: Future year for assessment.

        Returns:
            Dict with current and future suitability, trend, and details.
        """
        historical = self.data_loader.load_historical_climate_data(latitude, longitude)
        projected_climate = self.data_loader.get_projected_climate(
            latitude, longitude, target_year=target_year
        )

        # rainfall_avg and projected_rainfall are both monthly mm values – no
        # further division is needed.
        current_rainfall_monthly = historical["rainfall_avg"]
        future_rainfall_monthly = projected_climate["projected_rainfall"]

        return self.suitability_matcher.get_crop_adaptability(
            crop_name=crop_name,
            current_temp=historical["temp_avg"],
            current_rainfall_monthly=current_rainfall_monthly,
            future_temp=projected_climate["projected_temp"],
            future_rainfall_monthly=future_rainfall_monthly,
            soil_ph=soil_ph,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_explanation(
        top_crops: List[Dict],
        temp_change: float,
        rainfall_pct_change: float,
        climate_zone: str,
    ) -> str:
        """Generate a plain-English explanation for the recommendations."""
        if not top_crops:
            return "No suitable crops were found for the projected climate conditions."

        crop_names = ", ".join(c["crop"] for c in top_crops[:3])

        temp_phrase = f"temperatures are projected to rise by {temp_change:.1f}°C"
        rain_direction = "decrease" if rainfall_pct_change < 0 else "increase"
        rain_phrase = f"rainfall is expected to {rain_direction} by {abs(rainfall_pct_change):.0f}%"

        high_resilience = [c for c in top_crops if c.get("drought_tolerance", 0) >= 0.70]
        trait_phrase = ""
        if high_resilience:
            trait_phrase = (
                f" {', '.join(c['crop'] for c in high_resilience[:2])} "
                f"{'are' if len(high_resilience) > 1 else 'is'} particularly recommended "
                "because of their high drought and heat tolerance."
            )

        return (
            f"These crops are recommended because {temp_phrase} and {rain_phrase} "
            f"in this {climate_zone} region over the coming decade. "
            f"The top picks — {crop_names} — have strong suitability scores under "
            f"these projected conditions.{trait_phrase}"
        )

    @staticmethod
    def _build_trend_series(
        historical: Dict,
        ml_prediction: Dict,
        projected_climate: Dict,
        target_year: int,
    ) -> Dict:
        """Build simplified annual trend series for frontend charts.

        Produces ~10 data points spanning from 5 years ago to target_year.
        """
        import numpy as np

        current_year = 2024
        start_year = current_year - 5
        years = list(range(start_year, target_year + 1, max(1, (target_year - start_year) // 9)))

        # Historical averages from last 5 years of the 30-year series
        hist_temps = np.array(historical["temperature_monthly"][-60:])
        hist_rains = np.array(historical["rainfall_monthly"][-60:])
        hist_temp_by_year = [float(np.mean(hist_temps[i * 12: (i + 1) * 12])) for i in range(5)]
        hist_rain_by_year = [float(np.mean(hist_rains[i * 12: (i + 1) * 12])) for i in range(5)]

        temp_series = []
        rain_series = []

        for i, year in enumerate(years):
            if year <= current_year:
                idx = i if i < len(hist_temp_by_year) else -1
                temp_series.append({"year": year, "value": round(hist_temp_by_year[idx], 1)})
                rain_series.append({"year": year, "value": round(hist_rain_by_year[idx], 1)})
            else:
                # Interpolate between current and projected
                frac = (year - current_year) / max(target_year - current_year, 1)
                proj_temp = projected_climate["projected_temp"]
                # projected_rainfall is already a monthly mm average
                proj_rain_monthly = projected_climate["projected_rainfall"]
                base_temp = float(np.mean(hist_temps[-12:]))
                base_rain = float(np.mean(hist_rains[-12:]))
                temp_series.append({
                    "year": year,
                    "value": round(base_temp + frac * (proj_temp - base_temp), 1),
                })
                rain_series.append({
                    "year": year,
                    "value": round(base_rain + frac * (proj_rain_monthly - base_rain), 1),
                })

        return {
            "temperature_trend": temp_series,
            "rainfall_trend": rain_series,
        }
