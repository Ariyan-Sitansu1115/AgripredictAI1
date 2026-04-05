"""
Climate-Resilient Crop Recommendation API

Endpoints:
  POST /climate/predict/future-crops   – Main prediction endpoint
  GET  /climate/trends/{lat}/{lon}     – Climate trend data for a location
  POST /climate/crop-adaptability     – Assess a specific crop under future climate
"""
import logging

from fastapi import APIRouter, HTTPException, Path, status

from app.engines.crop_recommendation_engine import CropRecommendationEngine
from app.schemas.climate_schema import (
    CropAdaptabilityRequest,
    CropAdaptabilityResponse,
    ClimateTrendsResponse,
    FutureCropRequest,
    FutureCropResponse,
    ClimateTrendPoint,
)

router = APIRouter()
logger = logging.getLogger("climate_routes")

# Module-level engine instance (shared across requests for performance)
_engine = CropRecommendationEngine()


# ---------------------------------------------------------------------------
# POST /climate/predict/future-crops
# ---------------------------------------------------------------------------

@router.post(
    "/predict/future-crops",
    response_model=FutureCropResponse,
    summary="Predict climate-resilient crops",
    description=(
        "Accepts farm location (lat/lon) and soil parameters, runs the "
        "ensemble ML pipeline, and returns the top crops suited for projected "
        "climate conditions 5–10 years from now."
    ),
)
def predict_future_crops(payload: FutureCropRequest) -> FutureCropResponse:
    """Generate climate-resilient crop recommendations for a location."""
    logger.info(
        "predict_future_crops | year=%d",
        payload.target_year,
    )

    try:
        result = _engine.recommend(
            latitude=payload.latitude,
            longitude=payload.longitude,
            soil_ph=payload.soil_ph,
            nitrogen=payload.nitrogen,
            phosphorus=payload.phosphorus,
            potassium=payload.potassium,
            target_year=payload.target_year,
            top_n=payload.top_n,
        )
    except Exception as exc:
        logger.exception("Error generating crop recommendations: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate crop recommendations. Please try again.",
        ) from exc

    return FutureCropResponse(**result)


# ---------------------------------------------------------------------------
# GET /climate/trends/{lat}/{lon}
# ---------------------------------------------------------------------------

@router.get(
    "/trends/{lat}/{lon}",
    response_model=ClimateTrendsResponse,
    summary="Get climate trends for a location",
    description=(
        "Returns historical climate averages and IPCC-based projections "
        "for 2030 and 2050 for a given latitude/longitude."
    ),
)
def get_climate_trends(
    lat: float = Path(..., ge=-90, le=90, description="Latitude"),
    lon: float = Path(..., ge=-180, le=180, description="Longitude"),
) -> ClimateTrendsResponse:
    """Retrieve climate trend data for a location."""
    logger.info("get_climate_trends requested")

    try:
        loader = _engine.data_loader
        historical = loader.load_historical_climate_data(lat, lon)
        proj_2030 = loader.get_projected_climate(lat, lon, target_year=2030)
        proj_2050 = loader.get_projected_climate(lat, lon, target_year=2050)
        climate_zone = loader.get_climate_zone(lat, historical["temp_avg"], historical["rainfall_avg"])

        # Build simple trend series from historical + projections
        trend_result = _engine._build_trend_series(  # noqa: SLF001
            historical,
            {},
            proj_2030,
            2030,
        )

        temp_trend = [ClimateTrendPoint(**p) for p in trend_result["temperature_trend"]]
        rain_trend = [ClimateTrendPoint(**p) for p in trend_result["rainfall_trend"]]

        return ClimateTrendsResponse(
            latitude=lat,
            longitude=lon,
            historical_temp_avg=round(historical["temp_avg"], 2),
            historical_rainfall_avg=round(historical["rainfall_avg"], 2),
            projected_temp_2030=round(proj_2030["projected_temp"], 2),
            projected_temp_2050=round(proj_2050["projected_temp"], 2),
            projected_rainfall_2030=round(proj_2030["projected_rainfall"], 2),
            projected_rainfall_2050=round(proj_2050["projected_rainfall"], 2),
            climate_zone=climate_zone,
            temperature_trend=temp_trend,
            rainfall_trend=rain_trend,
        )

    except Exception as exc:
        logger.exception("Error retrieving climate trends: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve climate trends.",
        ) from exc


# ---------------------------------------------------------------------------
# POST /climate/crop-adaptability
# ---------------------------------------------------------------------------

@router.post(
    "/crop-adaptability",
    response_model=CropAdaptabilityResponse,
    summary="Assess crop adaptability under future climate",
    description=(
        "Evaluates how a specific crop's suitability changes between current "
        "and projected future climate conditions for a given location."
    ),
)
def check_crop_adaptability(payload: CropAdaptabilityRequest) -> CropAdaptabilityResponse:
    """Assess how a specific crop adapts to future climate conditions."""
    logger.info("check_crop_adaptability | crop=%s year=%d", payload.crop_name, payload.target_year)

    try:
        result = _engine.check_crop_adaptability(
            crop_name=payload.crop_name,
            latitude=payload.latitude,
            longitude=payload.longitude,
            soil_ph=payload.soil_ph,
            nitrogen=payload.nitrogen,
            phosphorus=payload.phosphorus,
            potassium=payload.potassium,
            target_year=payload.target_year,
        )
    except Exception as exc:
        logger.exception("Error assessing crop adaptability: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assess crop adaptability.",
        ) from exc

    if result.get("current_suitability") == 0.0 and result.get("future_suitability") == 0.0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crop '{payload.crop_name}' not found in the crop database.",
        )

    return CropAdaptabilityResponse(**result)
