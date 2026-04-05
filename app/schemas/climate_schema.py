"""Pydantic schemas for the Climate-Resilient Crop Recommendation Engine."""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class FutureCropRequest(BaseModel):
    """Input payload for the POST /predict/future-crops endpoint."""

    latitude: float = Field(
        ..., ge=-90, le=90, description="Farm latitude in decimal degrees."
    )
    longitude: float = Field(
        ..., ge=-180, le=180, description="Farm longitude in decimal degrees."
    )
    soil_ph: float = Field(
        default=6.5, ge=3.5, le=9.5, description="Soil pH value."
    )
    nitrogen: float = Field(
        default=80, ge=0, le=500, description="Soil nitrogen content (kg/ha)."
    )
    phosphorus: float = Field(
        default=45, ge=0, le=500, description="Soil phosphorus content (kg/ha)."
    )
    potassium: float = Field(
        default=50, ge=0, le=500, description="Soil potassium content (kg/ha)."
    )
    target_year: int = Field(
        default=2035,
        ge=2025,
        le=2100,
        description="Future year for climate projection (2025–2100).",
    )
    top_n: int = Field(
        default=5, ge=1, le=15, description="Number of top crops to return."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "latitude": 20.2961,
                "longitude": 85.8245,
                "soil_ph": 6.5,
                "nitrogen": 80,
                "phosphorus": 45,
                "potassium": 50,
                "target_year": 2035,
                "top_n": 5,
            }
        }
    }


class CropAdaptabilityRequest(BaseModel):
    """Input payload for the POST /crop-adaptability endpoint."""

    crop_name: str = Field(..., description="Name of the crop to assess.")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    soil_ph: float = Field(default=6.5, ge=3.5, le=9.5)
    nitrogen: float = Field(default=80, ge=0, le=500)
    phosphorus: float = Field(default=45, ge=0, le=500)
    potassium: float = Field(default=50, ge=0, le=500)
    target_year: int = Field(default=2035, ge=2025, le=2100)


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class RecommendedCrop(BaseModel):
    """A single crop recommendation with scores and planting info."""

    crop: str
    resilience_score: float = Field(..., ge=0, le=1)
    planting_season: str
    expected_yield: int = Field(..., description="Expected yield (kg/ha).")
    description: str
    temperature_score: float
    rainfall_score: float
    ph_score: float
    drought_tolerance: float
    heat_tolerance: float


class ClimateTrendPoint(BaseModel):
    """Single data point in a climate trend series."""

    year: int
    value: float


class FutureClimateSummary(BaseModel):
    """Summary of projected climate changes."""

    temperature_change: str
    rainfall_variation: str
    growing_season_change: str
    climate_zone: str
    confidence_score: float
    projected_temp: float
    projected_rainfall_monthly: float


class ClimateTrends(BaseModel):
    """Temperature and rainfall trend series for visualisation."""

    temperature_trend: List[ClimateTrendPoint]
    rainfall_trend: List[ClimateTrendPoint]


class FutureCropResponse(BaseModel):
    """Response from POST /predict/future-crops."""

    recommended_crops: List[RecommendedCrop]
    future_climate_summary: FutureClimateSummary
    explanation: str
    climate_trends: ClimateTrends


class CropAdaptabilityResponse(BaseModel):
    """Response from POST /crop-adaptability."""

    crop: str
    current_suitability: float
    future_suitability: float
    suitability_change: float
    adaptability_trend: str
    is_climate_resilient: bool
    details: Optional[Dict] = None


class ClimateTrendsResponse(BaseModel):
    """Response from GET /climate-trends/{lat}/{lon}."""

    latitude: float
    longitude: float
    historical_temp_avg: float
    historical_rainfall_avg: float
    projected_temp_2030: Optional[float] = None
    projected_temp_2050: Optional[float] = None
    projected_rainfall_2030: Optional[float] = None
    projected_rainfall_2050: Optional[float] = None
    climate_zone: str
    temperature_trend: List[ClimateTrendPoint]
    rainfall_trend: List[ClimateTrendPoint]
