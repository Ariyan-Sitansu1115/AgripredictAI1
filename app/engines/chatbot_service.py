"""
Farmer Assistant Chatbot Engine

A fully standalone, knowledge-based chatbot for agricultural queries.
Does not require any external AI API – all intelligence is embedded in
the knowledge base and rule-based intent system.

Key capabilities:
  - Intent detection (crop recommendation, price, comparison, risk, season)
  - 20+ crop knowledge base (season, rainfall, temperature, pH, fertilizer, yield, regions)
  - Market price database with trends
  - Context-aware conversation history
  - Multi-crop comparison
  - Risk and profitability analysis
  - Seasonal planning assistance
  - Follow-up suggestion generation
"""
from __future__ import annotations

import logging
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("chatbot_engine")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Maps numeric month → season name used in the crop DB
_MONTH_TO_SEASON: Dict[int, str] = {
    1: "Rabi", 2: "Rabi", 3: "Rabi",
    4: "Summer", 5: "Summer", 6: "Kharif",
    7: "Kharif", 8: "Kharif", 9: "Kharif",
    10: "Rabi", 11: "Rabi", 12: "Rabi",
}

# Readable month names
_MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

# Price forecast multipliers (assumes ±2% weekly change when trend is UP/DOWN)
_PRICE_TREND_MULTIPLIER_UP: float = 1.02
_PRICE_TREND_MULTIPLIER_DOWN: float = 0.98
_PRICE_TREND_MULTIPLIER_STABLE: float = 1.0
# Number of weekly periods for monthly forecast (approx. 4.3 weeks per month, rounded to 3)
_PRICE_FORECAST_WEEKS_IN_MONTH: int = 3

# Divisor to convert ₹ per hectare revenue to thousands (₹K) for display
_REVENUE_DISPLAY_DIVISOR: int = 1000


# ---------------------------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------------------------

def _initialize_knowledge_base() -> Dict[str, Dict[str, Any]]:
    """Build and return the comprehensive crop knowledge base."""
    return {
        "Rice": {
            "season": "Kharif (June–July)",
            "season_key": "Kharif",
            "planting_months": [6, 7],
            "harvest_months": [10, 11],
            "rainfall_mm": (1000, 2500),
            "temperature_c": (20, 30),
            "soil_ph": (5.5, 7.0),
            "fertilizer": "NPK 120:60:60 kg/ha",
            "yield_kg_ha": (5000, 6000),
            "regions": ["Odisha", "West Bengal", "Punjab", "Andhra Pradesh", "Tamil Nadu"],
            "description": "Staple cereal crop requiring standing water; main kharif crop in India.",
            "risks": ["Blast disease", "Brown planthopper", "Flood damage", "Water logging"],
            "profitability_score": 72,
        },
        "Wheat": {
            "season": "Rabi (October–November)",
            "season_key": "Rabi",
            "planting_months": [10, 11],
            "harvest_months": [3, 4],
            "rainfall_mm": (300, 900),
            "temperature_c": (10, 25),
            "soil_ph": (6.0, 7.5),
            "fertilizer": "NPK 120:60:40 kg/ha",
            "yield_kg_ha": (3500, 4500),
            "regions": ["Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Rajasthan"],
            "description": "Key rabi cereal; needs cool weather and moderate rainfall.",
            "risks": ["Rust disease", "Aphids", "Lodging", "Terminal heat stress"],
            "profitability_score": 68,
        },
        "Maize": {
            "season": "Kharif (June) / Rabi (October)",
            "season_key": "Kharif",
            "planting_months": [6, 10],
            "harvest_months": [9, 1],
            "rainfall_mm": (600, 1500),
            "temperature_c": (18, 32),
            "soil_ph": (5.8, 7.0),
            "fertilizer": "NPK 120:60:40 kg/ha",
            "yield_kg_ha": (4000, 5000),
            "regions": ["Karnataka", "Andhra Pradesh", "Bihar", "Rajasthan", "Madhya Pradesh"],
            "description": "Versatile cereal grown in both kharif and rabi seasons.",
            "risks": ["Fall armyworm", "Stalk rot", "Drought", "Waterlogging"],
            "profitability_score": 70,
        },
        "Millet": {
            "season": "Kharif (June–July)",
            "season_key": "Kharif",
            "planting_months": [6, 7],
            "harvest_months": [9, 10],
            "rainfall_mm": (300, 600),
            "temperature_c": (25, 35),
            "soil_ph": (6.0, 7.5),
            "fertilizer": "NPK 60:30:30 kg/ha",
            "yield_kg_ha": (1500, 2500),
            "regions": ["Rajasthan", "Gujarat", "Maharashtra", "Uttar Pradesh"],
            "description": "Drought-tolerant coarse cereal for drylands.",
            "risks": ["Downy mildew", "Smut", "Aphids"],
            "profitability_score": 55,
        },
        "Cotton": {
            "season": "Kharif (May–June)",
            "season_key": "Kharif",
            "planting_months": [5, 6],
            "harvest_months": [10, 11, 12],
            "rainfall_mm": (600, 1200),
            "temperature_c": (25, 35),
            "soil_ph": (6.0, 8.0),
            "fertilizer": "NPK 120:60:60 kg/ha",
            "yield_kg_ha": (1500, 2000),
            "regions": ["Gujarat", "Maharashtra", "Telangana", "Punjab", "Haryana"],
            "description": "Cash crop; major fibre crop grown in black cotton soil regions.",
            "risks": ["Bollworm", "Whitefly", "Drought", "Excessive rain during flowering"],
            "profitability_score": 78,
        },
        "Gram (Chickpea)": {
            "season": "Rabi (October–November)",
            "season_key": "Rabi",
            "planting_months": [10, 11],
            "harvest_months": [2, 3],
            "rainfall_mm": (400, 800),
            "temperature_c": (15, 25),
            "soil_ph": (6.0, 8.0),
            "fertilizer": "NPK 20:50:40 kg/ha",
            "yield_kg_ha": (1200, 2000),
            "regions": ["Madhya Pradesh", "Rajasthan", "Maharashtra", "Uttar Pradesh"],
            "description": "Important pulse crop; fixes nitrogen and improves soil fertility.",
            "risks": ["Wilt", "Blight", "Pod borer"],
            "profitability_score": 65,
        },
        "Pigeon Pea": {
            "season": "Kharif (June–July)",
            "season_key": "Kharif",
            "planting_months": [6, 7],
            "harvest_months": [11, 12],
            "rainfall_mm": (600, 1500),
            "temperature_c": (18, 30),
            "soil_ph": (5.5, 7.5),
            "fertilizer": "NPK 20:50:30 kg/ha",
            "yield_kg_ha": (1000, 1800),
            "regions": ["Maharashtra", "Uttar Pradesh", "Madhya Pradesh", "Karnataka"],
            "description": "Arhar/Tur; major kharif pulse crop in India.",
            "risks": ["Sterility mosaic", "Wilt", "Pod fly"],
            "profitability_score": 63,
        },
        "Tomato": {
            "season": "Summer / Rabi",
            "season_key": "Summer",
            "planting_months": [6, 10, 11, 1],
            "harvest_months": [9, 1, 3],
            "rainfall_mm": (600, 1200),
            "temperature_c": (18, 28),
            "soil_ph": (6.0, 7.0),
            "fertilizer": "NPK 100:60:60 kg/ha",
            "yield_kg_ha": (25000, 35000),
            "regions": ["Maharashtra", "Andhra Pradesh", "Karnataka", "Odisha", "Bihar"],
            "description": "High-value vegetable crop with multiple growing seasons.",
            "risks": ["Early blight", "Late blight", "Tomato leaf curl virus", "Fruit borer"],
            "profitability_score": 80,
        },
        "Potato": {
            "season": "Rabi (October–November)",
            "season_key": "Rabi",
            "planting_months": [10, 11],
            "harvest_months": [1, 2],
            "rainfall_mm": (600, 1000),
            "temperature_c": (10, 22),
            "soil_ph": (5.5, 6.5),
            "fertilizer": "NPK 180:120:120 kg/ha",
            "yield_kg_ha": (25000, 35000),
            "regions": ["Uttar Pradesh", "West Bengal", "Bihar", "Punjab", "Gujarat"],
            "description": "Important tuber crop; high yield and market demand.",
            "risks": ["Late blight", "Bacterial wilt", "Aphids", "Cut worm"],
            "profitability_score": 75,
        },
        "Onion": {
            "season": "Rabi (October–November)",
            "season_key": "Rabi",
            "planting_months": [10, 11],
            "harvest_months": [2, 3],
            "rainfall_mm": (500, 700),
            "temperature_c": (15, 25),
            "soil_ph": (6.0, 7.5),
            "fertilizer": "NPK 100:50:50 kg/ha",
            "yield_kg_ha": (15000, 25000),
            "regions": ["Maharashtra", "Karnataka", "Madhya Pradesh", "Gujarat", "Rajasthan"],
            "description": "High value vegetable crop with large domestic and export demand.",
            "risks": ["Purple blotch", "Thrips", "Price volatility"],
            "profitability_score": 72,
        },
        "Mango": {
            "season": "Summer (March–June)",
            "season_key": "Summer",
            "planting_months": [6, 7],
            "harvest_months": [4, 5, 6],
            "rainfall_mm": (750, 2500),
            "temperature_c": (24, 35),
            "soil_ph": (5.5, 7.5),
            "fertilizer": "NPK 1000:500:1000 g/tree",
            "yield_kg_ha": (10000, 20000),
            "regions": ["Andhra Pradesh", "Uttar Pradesh", "Maharashtra", "Bihar", "Karnataka"],
            "description": "King of fruits; perennial crop with high export value.",
            "risks": ["Mango hopper", "Powdery mildew", "Anthracnose", "Irregular bearing"],
            "profitability_score": 85,
        },
        "Papaya": {
            "season": "Year-round",
            "season_key": "Kharif",
            "planting_months": [6, 7, 8],
            "harvest_months": [9, 10, 11],
            "rainfall_mm": (1000, 2000),
            "temperature_c": (20, 35),
            "soil_ph": (6.0, 7.0),
            "fertilizer": "NPK 200:200:400 g/plant",
            "yield_kg_ha": (30000, 50000),
            "regions": ["Andhra Pradesh", "Gujarat", "West Bengal", "Karnataka", "Maharashtra"],
            "description": "Fast-growing fruit crop; fruit and leaf have medicinal value.",
            "risks": ["Papaya ringspot virus", "Phytophthora rot", "Mealybug"],
            "profitability_score": 82,
        },
        "Banana": {
            "season": "Year-round",
            "season_key": "Kharif",
            "planting_months": [6, 7],
            "harvest_months": [3, 4, 5],
            "rainfall_mm": (1000, 2200),
            "temperature_c": (20, 35),
            "soil_ph": (6.0, 7.5),
            "fertilizer": "NPK 200:60:300 g/plant",
            "yield_kg_ha": (25000, 40000),
            "regions": ["Tamil Nadu", "Maharashtra", "Andhra Pradesh", "Gujarat", "Kerala"],
            "description": "Tropical fruit crop; India is world's largest producer.",
            "risks": ["Panama wilt", "Sigatoka", "Bunchy top virus", "Weevils"],
            "profitability_score": 78,
        },
        "Sunflower": {
            "season": "Rabi (October) / Kharif (June)",
            "season_key": "Rabi",
            "planting_months": [6, 10],
            "harvest_months": [9, 1],
            "rainfall_mm": (500, 750),
            "temperature_c": (18, 30),
            "soil_ph": (6.0, 7.5),
            "fertilizer": "NPK 80:60:60 kg/ha",
            "yield_kg_ha": (1500, 2200),
            "regions": ["Karnataka", "Andhra Pradesh", "Maharashtra", "Tamil Nadu"],
            "description": "Important oilseed crop; short duration and drought tolerant.",
            "risks": ["Alternaria blight", "Sclerotinia rot", "Aphids"],
            "profitability_score": 67,
        },
        "Groundnut": {
            "season": "Kharif (June) / Rabi (November)",
            "season_key": "Kharif",
            "planting_months": [6, 11],
            "harvest_months": [9, 2],
            "rainfall_mm": (500, 1200),
            "temperature_c": (22, 30),
            "soil_ph": (6.0, 7.0),
            "fertilizer": "NPK 20:60:60 kg/ha",
            "yield_kg_ha": (1500, 2500),
            "regions": ["Gujarat", "Rajasthan", "Andhra Pradesh", "Tamil Nadu", "Karnataka"],
            "description": "Major oilseed crop; good nitrogen fixer; edible oil and protein source.",
            "risks": ["Tikka disease", "Aflatoxin", "Pod borer", "Thrips"],
            "profitability_score": 70,
        },
        "Soybean": {
            "season": "Kharif (June–July)",
            "season_key": "Kharif",
            "planting_months": [6, 7],
            "harvest_months": [9, 10],
            "rainfall_mm": (600, 1000),
            "temperature_c": (20, 30),
            "soil_ph": (6.0, 7.0),
            "fertilizer": "NPK 30:80:40 kg/ha",
            "yield_kg_ha": (2000, 3000),
            "regions": ["Madhya Pradesh", "Maharashtra", "Rajasthan", "Karnataka"],
            "description": "Versatile oilseed and protein crop; short duration kharif crop.",
            "risks": ["Yellow mosaic virus", "Girdle beetle", "Pod borer"],
            "profitability_score": 66,
        },
        "Sugarcane": {
            "season": "Year-round (Feb–March planting)",
            "season_key": "Kharif",
            "planting_months": [2, 3, 10, 11],
            "harvest_months": [10, 11, 12, 1],
            "rainfall_mm": (1000, 1500),
            "temperature_c": (20, 35),
            "soil_ph": (6.0, 8.0),
            "fertilizer": "NPK 250:60:120 kg/ha",
            "yield_kg_ha": (70000, 90000),
            "regions": ["Uttar Pradesh", "Maharashtra", "Karnataka", "Tamil Nadu", "Andhra Pradesh"],
            "description": "Long-duration industrial crop; primary source of sugar and jaggery.",
            "risks": ["Red rot", "Ratoon stunting disease", "Top borer", "Pyrilla"],
            "profitability_score": 74,
        },
        "Mustard": {
            "season": "Rabi (September–October)",
            "season_key": "Rabi",
            "planting_months": [9, 10],
            "harvest_months": [2, 3],
            "rainfall_mm": (300, 600),
            "temperature_c": (10, 22),
            "soil_ph": (6.0, 7.5),
            "fertilizer": "NPK 60:40:20 kg/ha",
            "yield_kg_ha": (1200, 2000),
            "regions": ["Rajasthan", "Uttar Pradesh", "Haryana", "West Bengal", "Gujarat"],
            "description": "Key rabi oilseed crop; cold-tolerant and water-efficient.",
            "risks": ["Alternaria blight", "Powdery mildew", "Aphids"],
            "profitability_score": 64,
        },
        "Turmeric": {
            "season": "Kharif (April–May)",
            "season_key": "Kharif",
            "planting_months": [4, 5],
            "harvest_months": [12, 1, 2],
            "rainfall_mm": (1000, 2000),
            "temperature_c": (20, 30),
            "soil_ph": (5.5, 7.0),
            "fertilizer": "NPK 60:40:120 kg/ha",
            "yield_kg_ha": (20000, 30000),
            "regions": ["Andhra Pradesh", "Odisha", "Tamil Nadu", "Maharashtra", "West Bengal"],
            "description": "High-value spice crop with medicinal and export value.",
            "risks": ["Rhizome rot", "Leaf blotch", "Thrips"],
            "profitability_score": 88,
        },
        "Ginger": {
            "season": "Kharif (April–May)",
            "season_key": "Kharif",
            "planting_months": [4, 5],
            "harvest_months": [11, 12, 1],
            "rainfall_mm": (1500, 3000),
            "temperature_c": (20, 30),
            "soil_ph": (5.5, 6.5),
            "fertilizer": "NPK 75:50:50 kg/ha",
            "yield_kg_ha": (15000, 25000),
            "regions": ["Kerala", "Meghalaya", "Arunachal Pradesh", "Odisha", "West Bengal"],
            "description": "Rhizomatous spice crop; high medicinal and culinary value.",
            "risks": ["Soft rot", "Bacterial wilt", "Shoot borer"],
            "profitability_score": 87,
        },
    }


def _initialize_market_prices() -> Dict[str, Dict[str, Any]]:
    """Return current market prices and trend data."""
    return {
        "Rice":            {"price": 45.0,  "unit": "kg",  "trend": "STABLE", "mssp": 2183},
        "Wheat":           {"price": 25.0,  "unit": "kg",  "trend": "UP",     "mssp": 2275},
        "Maize":           {"price": 20.0,  "unit": "kg",  "trend": "STABLE", "mssp": 1870},
        "Millet":          {"price": 18.0,  "unit": "kg",  "trend": "UP",     "mssp": 2500},
        "Cotton":          {"price": 75.0,  "unit": "kg",  "trend": "UP",     "mssp": 6620},
        "Gram (Chickpea)": {"price": 70.0,  "unit": "kg",  "trend": "STABLE", "mssp": 5440},
        "Pigeon Pea":      {"price": 75.0,  "unit": "kg",  "trend": "DOWN",   "mssp": 7000},
        "Tomato":          {"price": 30.0,  "unit": "kg",  "trend": "UP",     "mssp": None},
        "Potato":          {"price": 20.0,  "unit": "kg",  "trend": "STABLE", "mssp": None},
        "Onion":           {"price": 25.0,  "unit": "kg",  "trend": "DOWN",   "mssp": None},
        "Mango":           {"price": 60.0,  "unit": "kg",  "trend": "UP",     "mssp": None},
        "Papaya":          {"price": 15.0,  "unit": "kg",  "trend": "STABLE", "mssp": None},
        "Banana":          {"price": 20.0,  "unit": "kg",  "trend": "STABLE", "mssp": None},
        "Sunflower":       {"price": 55.0,  "unit": "kg",  "trend": "DOWN",   "mssp": 6760},
        "Groundnut":       {"price": 65.0,  "unit": "kg",  "trend": "STABLE", "mssp": 6377},
        "Soybean":         {"price": 45.0,  "unit": "kg",  "trend": "DOWN",   "mssp": 4600},
        "Sugarcane":       {"price": 3.5,   "unit": "kg",  "trend": "UP",     "mssp": 315},
        "Mustard":         {"price": 55.0,  "unit": "kg",  "trend": "UP",     "mssp": 5650},
        "Turmeric":        {"price": 130.0, "unit": "kg",  "trend": "UP",     "mssp": None},
        "Ginger":          {"price": 80.0,  "unit": "kg",  "trend": "STABLE", "mssp": None},
    }


# ---------------------------------------------------------------------------
# Intent patterns
# ---------------------------------------------------------------------------

_INTENT_PATTERNS: Dict[str, List[str]] = {
    "crop_recommendation": [
        r"what (should|can|shall) i (grow|plant|cultivate|sow)",
        r"(best|good|suitable|top) crop(s)?",
        r"(recommend|suggest).*(crop|plant|grow|cultivate)",
        r"best crop(s)? (for|in|at)",
        r"recommend.*crop",
        r"which crop",
        r"what crop",
        r"suggest.*crop",
        r"what (to|should) (grow|plant|cultivate)",
        r"crop(s)? (for|in|at|this|next)",
    ],
    "price_prediction": [
        r"(price|rate|cost|value) of",
        r"market (price|rate|trend)",
        r"(how much|what is).*(price|cost|rate|value)",
        r"selling price",
        r"current price",
        r"price (today|this week|this month)",
        r"msp|mssp|minimum support",
        r"market trend",
    ],
    "crop_comparison": [
        r"compare.*and",
        r"difference between",
        r"vs\.?",
        r"versus",
        r"(better|best) between",
        r"which is (better|more profitable|more suitable)",
        r"or.*grow",
    ],
    "risk_analysis": [
        r"risk(s)?",
        r"(disease|pest|problem|issue)",
        r"danger",
        r"(prevent|protection|protect|manage|control)",
        r"(safe|safety|secure)",
        r"how to (protect|prevent|control|manage)",
        r"profitability",
        r"is it (safe|profitable|risky)",
        r"(threat|concern|challenge)",
    ],
    "season_query": [
        r"(season|seasonal|time|month) (for|to|of)",
        r"(kharif|rabi|summer) (crop|season)",
        r"(when|which month) (to|for|should)",
        r"best time (to|for)",
        r"planting (time|season|month)",
        r"harvest (time|season|month)",
        r"what season",
        r"crop (calendar|schedule|planting)",
    ],
    "soil_query": [
        r"soil (type|ph|requirement|condition|quality)",
        r"(ph|nutrient|fertility|texture) (for|of)",
        r"what (type of )?soil",
        r"(clay|sandy|loamy|black|alluvial)",
    ],
    "fertilizer_query": [
        r"fertilizer",
        r"manure",
        r"(npk|nitrogen|phosphorus|potassium)",
        r"nutrient (requirement|management)",
        r"(urea|dap|mop)",
        r"how much (fertilizer|manure|npk)",
    ],
    "yield_query": [
        r"(yield|production|output|harvest)",
        r"how much (will|can|does) .*(produce|yield|give)",
        r"(kg|ton|quintal) per (hectare|ha|acre)",
        r"productivity",
    ],
}

# ---------------------------------------------------------------------------
# Crop name extraction helpers
# ---------------------------------------------------------------------------

_ALL_CROPS_LOWER: Dict[str, str] = {}  # populated lazily


def _build_crop_map(knowledge_base: Dict[str, Any]) -> Dict[str, str]:
    """Build a lowercase → canonical name lookup."""
    mapping: Dict[str, str] = {}
    aliases = {
        "rice": "Rice", "paddy": "Rice",
        "wheat": "Wheat", "gehun": "Wheat",
        "maize": "Maize", "corn": "Maize", "makka": "Maize",
        "millet": "Millet", "bajra": "Millet", "jowar": "Millet",
        "cotton": "Cotton", "kapas": "Cotton",
        "gram": "Gram (Chickpea)", "chickpea": "Gram (Chickpea)", "chana": "Gram (Chickpea)",
        "pigeon pea": "Pigeon Pea", "tur": "Pigeon Pea", "arhar": "Pigeon Pea",
        "tomato": "Tomato",
        "potato": "Potato", "aloo": "Potato",
        "onion": "Onion", "pyaz": "Onion",
        "mango": "Mango", "aam": "Mango",
        "papaya": "Papaya",
        "banana": "Banana", "kela": "Banana",
        "sunflower": "Sunflower",
        "groundnut": "Groundnut", "peanut": "Groundnut", "moongfali": "Groundnut",
        "soybean": "Soybean", "soya": "Soybean",
        "sugarcane": "Sugarcane", "ganna": "Sugarcane",
        "mustard": "Mustard", "sarson": "Mustard",
        "turmeric": "Turmeric", "haldi": "Turmeric",
        "ginger": "Ginger", "adrak": "Ginger",
    }
    for alias, canonical in aliases.items():
        mapping[alias] = canonical
    for crop in knowledge_base:
        mapping[crop.lower()] = crop
    return mapping


# ---------------------------------------------------------------------------
# Conversation history (in-memory)
# ---------------------------------------------------------------------------

_conversation_histories: Dict[str, List[Dict[str, Any]]] = {}
_HISTORY_LIMIT = 20


def _get_history(session_id: str) -> List[Dict[str, Any]]:
    return _conversation_histories.get(session_id, [])


def _add_to_history(session_id: str, role: str, content: str) -> None:
    if session_id not in _conversation_histories:
        _conversation_histories[session_id] = []
    _conversation_histories[session_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    # Keep only recent turns
    if len(_conversation_histories[session_id]) > _HISTORY_LIMIT:
        _conversation_histories[session_id] = _conversation_histories[session_id][-_HISTORY_LIMIT:]


def clear_history(session_id: str) -> None:
    """Clear conversation history for a session."""
    _conversation_histories.pop(session_id, None)


def get_history(session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Return recent conversation history for a session."""
    history = _get_history(session_id)
    return history[-limit:]


# ---------------------------------------------------------------------------
# Core chatbot class
# ---------------------------------------------------------------------------

class FarmerAssistantChatbot:
    """
    Rule-based, knowledge-driven farmer assistant chatbot.

    Processes natural language queries from farmers and returns structured
    responses with agricultural advice.  No external API required.
    """

    def __init__(self) -> None:
        self._kb = _initialize_knowledge_base()
        self._prices = _initialize_market_prices()
        self._crop_map = _build_crop_map(self._kb)
        logger.info("FarmerAssistantChatbot initialised with %d crops", len(self._kb))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_query(
        self,
        message: str,
        *,
        location: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process a user query and return a structured response.

        Returns:
            {
                "response": str,
                "intent": str,
                "suggestions": List[str],
                "data": Optional[dict],
                "session_id": str,
            }
        """
        if not session_id:
            session_id = str(uuid.uuid4())

        _add_to_history(session_id, "user", message)

        intent, crops = self._extract_intent(message)
        logger.debug("Intent: %s | Crops: %s | Location: %s", intent, crops, location)

        response_text, data = self._dispatch(intent, message, crops, location)

        suggestions = self._generate_suggestions(intent, crops, location)

        _add_to_history(session_id, "assistant", response_text)

        return {
            "response": response_text,
            "intent": intent,
            "crops": crops,
            "suggestions": suggestions,
            "data": data,
            "session_id": session_id,
        }

    # ------------------------------------------------------------------
    # Intent extraction
    # ------------------------------------------------------------------

    def _extract_intent(self, message: str) -> Tuple[str, List[str]]:
        """
        Detect intent and extract crop names from the user message.

        Returns (intent_name, list_of_crops).
        """
        msg_lower = message.lower()
        crops = self._extract_crop_names(msg_lower)

        # Check comparison intent first (needs 2 crops or explicit keyword)
        if len(crops) >= 2 or re.search(r"\bvs\.?\b|\bversus\b|\bcompare\b", msg_lower):
            return "crop_comparison", crops

        for intent, patterns in _INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, msg_lower):
                    return intent, crops

        return "general", crops

    def _extract_crop_names(self, message_lower: str) -> List[str]:
        """Extract canonical crop names from a lowercased message."""
        found: List[str] = []
        # Sort by length descending to prefer longer matches (e.g., "pigeon pea" before "pea")
        for alias in sorted(self._crop_map.keys(), key=len, reverse=True):
            if re.search(r"\b" + re.escape(alias) + r"\b", message_lower):
                canonical = self._crop_map[alias]
                if canonical not in found:
                    found.append(canonical)
        return found

    # ------------------------------------------------------------------
    # Response dispatcher
    # ------------------------------------------------------------------

    def _dispatch(
        self,
        intent: str,
        message: str,
        crops: List[str],
        location: Optional[str],
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        handlers = {
            "crop_recommendation": self._handle_crop_recommendation,
            "price_prediction":    self._handle_price_prediction,
            "crop_comparison":     self._handle_crop_comparison,
            "risk_analysis":       self._handle_risk_analysis,
            "season_query":        self._handle_season_query,
            "soil_query":          self._handle_soil_query,
            "fertilizer_query":    self._handle_fertilizer_query,
            "yield_query":         self._handle_yield_query,
        }
        handler = handlers.get(intent, self._handle_general_query)
        return handler(message, crops, location)

    # ------------------------------------------------------------------
    # Intent handlers
    # ------------------------------------------------------------------

    def _handle_crop_recommendation(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Recommend a crop based on season, location, and mentioned crops."""
        month = datetime.now().month
        current_season = _MONTH_TO_SEASON[month]
        month_name = _MONTH_NAMES[month]

        # If a specific crop was mentioned, give details for that crop
        if crops:
            crop = crops[0]
            info = self._kb.get(crop)
            if info:
                return self._format_crop_recommendation(crop, info, location), {
                    "crop": crop,
                    "season": info["season"],
                    "yield_range": info["yield_kg_ha"],
                    "profitability_score": info["profitability_score"],
                }

        # Otherwise recommend seasonal crops
        seasonal_crops = self._get_seasonal_crops(current_season)
        if location:
            seasonal_crops = self._filter_by_region(seasonal_crops, location)

        if not seasonal_crops:
            seasonal_crops = list(self._kb.keys())[:5]

        lines = [
            f"🌾 **Crop Recommendations for {month_name} ({current_season} Season)**",
            "",
        ]
        if location:
            lines.append(f"📍 Region: {location}")
            lines.append("")
        lines.append("**Top Recommended Crops:**")
        lines.append("")

        data_rows = []
        for i, crop_name in enumerate(seasonal_crops[:5], 1):
            info = self._kb[crop_name]
            price_info = self._prices.get(crop_name, {})
            price_str = f"₹{price_info.get('price', 'N/A')}/kg" if price_info else "N/A"
            lines.append(
                f"{i}. **{crop_name}** – {info['season']} | "
                f"Yield: {info['yield_kg_ha'][0]}–{info['yield_kg_ha'][1]} kg/ha | "
                f"Market: {price_str}"
            )
            data_rows.append({
                "crop": crop_name,
                "season": info["season"],
                "yield_kg_ha": info["yield_kg_ha"],
                "profitability_score": info["profitability_score"],
            })

        lines += [
            "",
            f"💡 *Currently it is {month_name}. "
            f"For best results, choose a crop suited to {current_season} season.*",
        ]

        return "\n".join(lines), {"season": current_season, "crops": data_rows}

    def _handle_price_prediction(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Return current market price and forecast for a crop."""
        if not crops:
            # List top crops with prices
            lines = ["💰 **Current Market Prices (per kg)**", ""]
            for crop, info in list(self._prices.items())[:8]:
                trend_icon = "📈" if info["trend"] == "UP" else ("📉" if info["trend"] == "DOWN" else "➡️")
                lines.append(f"• **{crop}**: ₹{info['price']}/kg {trend_icon} {info['trend']}")
            lines.append("")
            lines.append("Ask me about a specific crop for detailed price analysis!")
            return "\n".join(lines), None

        crop = crops[0]
        price_info = self._prices.get(crop)
        if not price_info:
            return (
                f"Sorry, I don't have current price data for **{crop}**. "
                "Please check your local APMC market for the latest rates.",
                None,
            )

        price = price_info["price"]
        trend = price_info["trend"]
        trend_icon = "📈" if trend == "UP" else ("📉" if trend == "DOWN" else "➡️")
        trend_pct = (
            _PRICE_TREND_MULTIPLIER_UP if trend == "UP" else
            (_PRICE_TREND_MULTIPLIER_DOWN if trend == "DOWN" else _PRICE_TREND_MULTIPLIER_STABLE)
        )

        forecast_week = round(price * trend_pct, 2)
        forecast_month = round(price * (trend_pct ** _PRICE_FORECAST_WEEKS_IN_MONTH), 2)

        mssp_line = ""
        if price_info.get("mssp"):
            mssp_per_kg = round(price_info["mssp"] / 100, 2)
            mssp_line = f"🏛️ MSP (Government): ₹{mssp_per_kg}/kg"

        recommendation = (
            "✅ **Good time to sell!**" if trend == "UP" else
            ("⚠️ Consider holding if possible." if trend == "DOWN" else
             "ℹ️ Prices are stable – standard selling window.")
        )

        response = (
            f"💰 **{crop} Market Price**\n\n"
            f"💵 Current Price: ₹{price}/kg\n"
            f"{trend_icon} Trend: **{trend}**\n"
        )
        if mssp_line:
            response += f"{mssp_line}\n"
        response += (
            f"\n📊 **Price Forecast:**\n"
            f"• Next Week: ₹{forecast_week}/kg\n"
            f"• Next Month: ₹{forecast_month}/kg\n\n"
            f"{recommendation}"
        )

        return response, {
            "crop": crop,
            "current_price": price,
            "trend": trend,
            "forecast_week": forecast_week,
            "forecast_month": forecast_month,
        }

    def _handle_crop_comparison(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Compare two or more crops side-by-side."""
        if len(crops) < 2:
            # Pick two common crops for demonstration
            crops = ["Rice", "Wheat"] if "rice" not in message.lower() else ["Wheat", "Maize"]

        crop_data = []
        for crop in crops[:3]:  # Compare up to 3 crops
            info = self._kb.get(crop, {})
            price_info = self._prices.get(crop, {})
            if info:
                crop_data.append((crop, info, price_info))

        if not crop_data:
            return "I couldn't find data for the requested crops.", None

        lines = [
            f"🌾 **Crop Comparison: {' vs '.join(c[0] for c in crop_data)}**",
            "",
        ]

        for crop, info, price_info in crop_data:
            trend_icon = (
                "📈" if price_info.get("trend") == "UP" else
                ("📉" if price_info.get("trend") == "DOWN" else "➡️")
            )
            lines += [
                f"**{crop}:**",
                f"  📅 Season: {info['season']}",
                f"  💧 Rainfall: {info['rainfall_mm'][0]}–{info['rainfall_mm'][1]} mm",
                f"  🌡️ Temperature: {info['temperature_c'][0]}–{info['temperature_c'][1]}°C",
                f"  📊 Yield: {info['yield_kg_ha'][0]}–{info['yield_kg_ha'][1]} kg/ha",
                f"  💰 Price: ₹{price_info.get('price', 'N/A')}/kg {trend_icon}",
                f"  ⭐ Profitability: {info['profitability_score']}/100",
                "",
            ]

        # Recommendation based on profitability score
        best = max(crop_data, key=lambda x: x[1].get("profitability_score", 0))
        lines += [
            f"✅ **Recommendation:** Based on current profitability score, "
            f"**{best[0]}** is the better choice.",
            "",
            "💡 *Final decision depends on your soil type, water availability, and local market access.*",
        ]

        return "\n".join(lines), {
            "crops": [
                {
                    "crop": c,
                    "profitability_score": i.get("profitability_score"),
                    "yield_kg_ha": i.get("yield_kg_ha"),
                    "price": p.get("price"),
                    "trend": p.get("trend"),
                }
                for c, i, p in crop_data
            ],
            "recommended": best[0],
        }

    def _handle_risk_analysis(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Provide risk and profitability analysis for a crop."""
        if not crops:
            return (
                "🛡️ **General Agricultural Risk Management Tips**\n\n"
                "1. **Crop Diversification** – Never depend on a single crop.\n"
                "2. **Crop Insurance** – Enroll in PMFBY for weather risk coverage.\n"
                "3. **IPM Practices** – Use Integrated Pest Management to reduce chemical costs.\n"
                "4. **Soil Health Cards** – Get your soil tested every 3 years.\n"
                "5. **Weather Alerts** – Sign up for IMD weather alerts via Meghdoot app.\n"
                "6. **Market Linkage** – Sell through FPOs or e-NAM platform for better prices.\n\n"
                "Ask about a specific crop for detailed risk analysis!",
                None,
            )

        crop = crops[0]
        info = self._kb.get(crop)
        if not info:
            return f"I don't have risk data for **{crop}**.", None

        score = info["profitability_score"]
        risk_level = "LOW" if score >= 75 else ("MEDIUM" if score >= 60 else "HIGH")
        risk_icon = "🟢" if risk_level == "LOW" else ("🟡" if risk_level == "MEDIUM" else "🔴")

        lines = [
            f"🛡️ **Risk & Profitability Analysis: {crop}**",
            "",
            f"{risk_icon} **Overall Risk Level:** {risk_level}",
            f"⭐ **Profitability Score:** {score}/100",
            "",
            "⚠️ **Key Risks:**",
        ]
        for i, risk in enumerate(info.get("risks", []), 1):
            lines.append(f"  {i}. {risk}")

        lines += [
            "",
            "🛡️ **Risk Mitigation Strategies:**",
            f"  • Use certified disease-resistant varieties.",
            f"  • Apply recommended NPK: {info['fertilizer']}",
            f"  • Maintain soil pH between {info['soil_ph'][0]} and {info['soil_ph'][1]}.",
            f"  • Ensure adequate drainage to prevent waterlogging.",
            f"  • Monitor crops regularly for early pest/disease signs.",
            f"  • Enroll in PMFBY crop insurance before deadline.",
            "",
            "📈 **Profitability Tips:**",
            f"  • Expected yield: {info['yield_kg_ha'][0]}–{info['yield_kg_ha'][1]} kg/ha",
            f"  • Grow in suitable regions: {', '.join(info['regions'][:3])}",
        ]

        price_info = self._prices.get(crop, {})
        if price_info:
            lines.append(f"  • Current market price: ₹{price_info['price']}/kg (Trend: {price_info['trend']})")

        return "\n".join(lines), {
            "crop": crop,
            "risk_level": risk_level,
            "profitability_score": score,
            "risks": info.get("risks", []),
        }

    def _handle_season_query(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Answer queries about seasonal planting and harvest times."""
        month = datetime.now().month
        current_season = _MONTH_TO_SEASON[month]

        # If a specific crop is mentioned
        if crops:
            crop = crops[0]
            info = self._kb.get(crop)
            if info:
                planting = [_MONTH_NAMES[m] for m in info["planting_months"]]
                harvest = [_MONTH_NAMES[m] for m in info["harvest_months"]]
                response = (
                    f"📅 **Seasonal Calendar for {crop}**\n\n"
                    f"🌱 **Season:** {info['season']}\n"
                    f"🌾 **Planting Time:** {', '.join(planting)}\n"
                    f"🚜 **Harvest Time:** {', '.join(harvest)}\n"
                    f"💧 **Rainfall Required:** {info['rainfall_mm'][0]}–{info['rainfall_mm'][1]} mm\n"
                    f"🌡️ **Ideal Temperature:** {info['temperature_c'][0]}–{info['temperature_c'][1]}°C\n\n"
                    f"📍 **Best Growing Regions:** {', '.join(info['regions'][:4])}"
                )
                return response, {
                    "crop": crop,
                    "season": info["season"],
                    "planting_months": planting,
                    "harvest_months": harvest,
                }

        # General season overview
        kharif_crops = self._get_seasonal_crops("Kharif")[:5]
        rabi_crops = self._get_seasonal_crops("Rabi")[:5]
        summer_crops = self._get_seasonal_crops("Summer")[:3]

        response = (
            f"📅 **Indian Crop Calendar**\n\n"
            f"🌧️ **Kharif Season (June–October):**\n"
            f"  {', '.join(kharif_crops)}\n\n"
            f"❄️ **Rabi Season (October–March):**\n"
            f"  {', '.join(rabi_crops)}\n\n"
            f"☀️ **Summer/Zaid Crops (March–June):**\n"
            f"  {', '.join(summer_crops)}\n\n"
            f"📍 **Currently ({_MONTH_NAMES[month]}):** It is {current_season} season.\n"
            f"Recommended crops: {', '.join(self._get_seasonal_crops(current_season)[:4])}"
        )
        return response, {
            "current_season": current_season,
            "current_month": _MONTH_NAMES[month],
            "kharif_crops": kharif_crops,
            "rabi_crops": rabi_crops,
        }

    def _handle_soil_query(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Answer soil-related queries."""
        if crops:
            crop = crops[0]
            info = self._kb.get(crop)
            if info:
                response = (
                    f"🧪 **Soil Requirements for {crop}**\n\n"
                    f"📊 **Soil pH:** {info['soil_ph'][0]} – {info['soil_ph'][1]}\n"
                    f"🌱 **Fertilizer:** {info['fertilizer']}\n"
                    f"💧 **Rainfall:** {info['rainfall_mm'][0]}–{info['rainfall_mm'][1]} mm\n\n"
                    f"💡 **Soil Tips:**\n"
                    f"  • Get a soil health card (SHC) for accurate nutrient data.\n"
                    f"  • Add organic matter/compost to improve soil structure.\n"
                    f"  • Use lime to raise pH or sulphur to lower pH if needed.\n"
                    f"  • Maintain good drainage to avoid waterlogging."
                )
                return response, {
                    "crop": crop,
                    "soil_ph": info["soil_ph"],
                    "fertilizer": info["fertilizer"],
                }

        return (
            "🧪 **General Soil Health Guide**\n\n"
            "**Soil pH Guide:**\n"
            "  • pH 5.5–6.5: Ideal for most vegetables and fruits\n"
            "  • pH 6.0–7.0: Ideal for rice, wheat, maize\n"
            "  • pH 6.0–8.0: Suitable for cotton, gram\n\n"
            "**Soil Types in India:**\n"
            "  • Alluvial – Wheat, Rice, Sugarcane\n"
            "  • Black Cotton – Cotton, Soybean, Sorghum\n"
            "  • Red – Groundnut, Cotton, Millets\n"
            "  • Laterite – Tea, Coffee, Cashew\n\n"
            "Ask about a specific crop for detailed soil requirements!",
            None,
        )

    def _handle_fertilizer_query(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Answer fertilizer and nutrient management queries."""
        if crops:
            crop = crops[0]
            info = self._kb.get(crop)
            if info:
                response = (
                    f"🌿 **Fertilizer Recommendation for {crop}**\n\n"
                    f"💊 **Recommended Dose:** {info['fertilizer']}\n\n"
                    f"📋 **Application Schedule:**\n"
                    f"  • Basal dose (at sowing): Apply P and K fully + 50% N\n"
                    f"  • 1st top-dressing (30 days): 25% N\n"
                    f"  • 2nd top-dressing (60 days): 25% N\n\n"
                    f"🌱 **Organic Alternatives:**\n"
                    f"  • FYM/Compost: 10–15 tonnes/ha\n"
                    f"  • Vermicompost: 2–3 tonnes/ha\n"
                    f"  • Biofertilizers: Rhizobium, Azotobacter\n\n"
                    f"⚠️ Always follow soil test results for precise doses."
                )
                return response, {
                    "crop": crop,
                    "fertilizer": info["fertilizer"],
                    "soil_ph_required": info["soil_ph"],
                }

        return (
            "🌿 **General Fertilizer Guide**\n\n"
            "• **Nitrogen (N):** Promotes leaf and stem growth – Urea, CAN\n"
            "• **Phosphorus (P):** Promotes root development – DAP, SSP\n"
            "• **Potassium (K):** Improves crop quality and disease resistance – MOP\n\n"
            "💡 **Best Practices:**\n"
            "  • Always base fertilizer use on soil test recommendations.\n"
            "  • Split nitrogen application to reduce losses.\n"
            "  • Combine chemical fertilizers with organic manure for best results.\n\n"
            "Ask about a specific crop for detailed fertilizer recommendations!",
            None,
        )

    def _handle_yield_query(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Answer yield-related queries."""
        if crops:
            crop = crops[0]
            info = self._kb.get(crop)
            if info:
                y_min, y_max = info["yield_kg_ha"]
                price_info = self._prices.get(crop, {})
                price = price_info.get("price", 0)
                revenue_min = round(y_min * price / _REVENUE_DISPLAY_DIVISOR, 0)
                revenue_max = round(y_max * price / _REVENUE_DISPLAY_DIVISOR, 0)
                response = (
                    f"📊 **Yield Information for {crop}**\n\n"
                    f"🌾 **Expected Yield:** {y_min:,} – {y_max:,} kg/ha\n"
                    f"💰 **Potential Revenue:** ₹{revenue_min:,.0f}K – ₹{revenue_max:,.0f}K per hectare\n"
                    f"  (at current market price of ₹{price}/kg)\n\n"
                    f"🚀 **Tips to Improve Yield:**\n"
                    f"  • Use HYV (High Yielding Varieties) certified seeds.\n"
                    f"  • Follow recommended {info['fertilizer']} application.\n"
                    f"  • Ensure proper irrigation – aim for {info['rainfall_mm'][0]}–{info['rainfall_mm'][1]} mm water.\n"
                    f"  • Timely sowing during {info['season']}.\n"
                    f"  • Regular pest and disease monitoring.\n"
                    f"  • Practice crop rotation."
                )
                return response, {
                    "crop": crop,
                    "yield_kg_ha": {"min": y_min, "max": y_max},
                    "revenue_per_ha_inr_k": {"min": revenue_min, "max": revenue_max},
                    "current_price_per_kg": price,
                }

        return (
            "📊 **Crop Yield Guide**\n\n"
            "Average yields for major crops (kg/ha):\n\n"
            + "\n".join(
                f"• **{crop}:** {info['yield_kg_ha'][0]:,}–{info['yield_kg_ha'][1]:,} kg/ha"
                for crop, info in list(self._kb.items())[:8]
            )
            + "\n\nAsk about a specific crop for detailed yield and revenue information!",
            None,
        )

    def _handle_general_query(
        self, message: str, crops: List[str], location: Optional[str]
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Handle general or unrecognized queries with a helpful response."""
        # If a crop was mentioned, give basic info
        if crops:
            crop = crops[0]
            info = self._kb.get(crop)
            if info:
                return self._format_crop_recommendation(crop, info, location), {
                    "crop": crop,
                    "season": info["season"],
                    "yield_range": info["yield_kg_ha"],
                }

        return (
            "👋 **Welcome to AgriPredict Farmer Assistant!**\n\n"
            "I can help you with:\n"
            "🌾 **Crop Recommendations** – Best crops for your region/season\n"
            "💰 **Market Prices** – Current prices and price trends\n"
            "⚖️ **Crop Comparison** – Compare profitability of multiple crops\n"
            "🛡️ **Risk Analysis** – Pest, disease, and market risk management\n"
            "📅 **Seasonal Planning** – Kharif, Rabi, and Summer crop calendars\n"
            "🧪 **Soil & Fertilizer** – Soil requirements and fertilizer doses\n"
            "📊 **Yield Information** – Expected yield and revenue estimates\n\n"
            "**Try asking:**\n"
            "• \"What should I grow in Odisha this month?\"\n"
            "• \"Compare rice and wheat\"\n"
            "• \"What is the price of cotton?\"\n"
            "• \"Analyze risks for tomato farming\"",
            None,
        )

    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------

    def _format_crop_recommendation(
        self, crop: str, info: Dict[str, Any], location: Optional[str]
    ) -> str:
        """Format a detailed crop recommendation card."""
        price_info = self._prices.get(crop, {})
        price_line = f"💰 Current Market Price: ₹{price_info['price']}/kg" if price_info else ""

        return (
            f"🌾 **{crop} – Crop Details**\n\n"
            f"📅 Best Season: {info['season']}\n"
            f"💧 Rainfall Needed: {info['rainfall_mm'][0]}–{info['rainfall_mm'][1]} mm\n"
            f"🌡️ Temperature Range: {info['temperature_c'][0]}–{info['temperature_c'][1]}°C\n"
            f"🧪 Soil pH: {info['soil_ph'][0]}–{info['soil_ph'][1]}\n"
            f"🥗 Recommended Fertilizer: {info['fertilizer']}\n"
            f"📊 Expected Yield: {info['yield_kg_ha'][0]:,}–{info['yield_kg_ha'][1]:,} kg/ha\n"
            f"📍 Best Regions: {', '.join(info['regions'][:4])}\n"
            + (f"{price_line}\n" if price_line else "")
            + f"\nℹ️ {info['description']}"
        )

    # ------------------------------------------------------------------
    # Suggestion generation
    # ------------------------------------------------------------------

    def _generate_suggestions(
        self, intent: str, crops: List[str], location: Optional[str]
    ) -> List[str]:
        """Generate context-aware follow-up suggestions."""
        suggestions: List[str] = []

        if intent == "crop_recommendation" and crops:
            crop = crops[0]
            suggestions = [
                f"What is the market price of {crop}?",
                f"What are the risks for {crop} farming?",
                f"What fertilizer should I use for {crop}?",
            ]
        elif intent == "price_prediction" and crops:
            crop = crops[0]
            alternatives = [c for c in self._kb if c != crop][:2]
            suggestions = [
                f"Compare {crop} with {alternatives[0] if alternatives else 'Wheat'}",
                f"What is the risk analysis for {crop}?",
                "Show me all current market prices",
            ]
        elif intent == "crop_comparison":
            suggestions = [
                "What crop should I grow this season?",
                "Show me market price trends",
                "What are the soil requirements?",
            ]
        elif intent == "risk_analysis" and crops:
            crop = crops[0]
            suggestions = [
                f"What fertilizer should I use for {crop}?",
                f"What is the expected yield for {crop}?",
                f"What is the market price of {crop}?",
            ]
        elif intent == "season_query":
            month = datetime.now().month
            season = _MONTH_TO_SEASON[month]
            suggestions = [
                f"Best crops for {season} season",
                "Compare Kharif and Rabi crops",
                "What crop gives the best profit?",
            ]
        else:
            suggestions = [
                "What crop should I grow this month?",
                "Compare rice and wheat",
                "Check risks for cotton farming",
            ]

        return suggestions[:3]

    # ------------------------------------------------------------------
    # Seasonal helpers
    # ------------------------------------------------------------------

    def _get_seasonal_crops(self, season: str) -> List[str]:
        """Return crops suitable for the given season, sorted by profitability."""
        crops = [
            name for name, info in self._kb.items()
            if info.get("season_key") == season
        ]
        crops.sort(key=lambda c: self._kb[c].get("profitability_score", 0), reverse=True)
        return crops

    def _filter_by_region(self, crops: List[str], location: str) -> List[str]:
        """Filter crops by region/state suitability."""
        location_lower = location.lower()
        matched = [
            c for c in crops
            if any(location_lower in r.lower() for r in self._kb[c].get("regions", []))
        ]
        return matched if matched else crops


# ---------------------------------------------------------------------------
# Module-level singleton and convenience function
# ---------------------------------------------------------------------------

_chatbot_instance: Optional[FarmerAssistantChatbot] = None


def _get_chatbot() -> FarmerAssistantChatbot:
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = FarmerAssistantChatbot()
    return _chatbot_instance


def process_query(
    message: str,
    *,
    location: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Module-level convenience wrapper around :class:`FarmerAssistantChatbot`.

    Returns the same dict as ``FarmerAssistantChatbot.process_query``.
    """
    return _get_chatbot().process_query(
        message,
        location=location,
        user_id=user_id,
        session_id=session_id,
    )
