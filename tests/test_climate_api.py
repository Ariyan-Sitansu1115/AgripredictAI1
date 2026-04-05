"""
Tests for the Climate-Resilient Crop Recommendation Engine.

Covers:
  - climate_data_loader  : data loading, caching, climate zone assignment
  - climate_prediction_model : future climate prediction output shape
  - crop_recommendation_engine : scoring, ranking, explanation
  - climate_api (FastAPI routes) : HTTP endpoint contract
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.climate_api import router as climate_router
from app.climate.climate_data_loader import load_climate_data, _cache_key
from app.climate.climate_prediction_model import predict_future_climate
from app.climate.crop_recommendation_engine import (
    CROP_SUITABILITY,
    recommend_crops,
    _resilience_score,
    _score_in_range,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_client() -> TestClient:
    """Create a minimal FastAPI test app with only the climate router."""
    app = FastAPI()
    app.include_router(climate_router, prefix="/api/predict")
    return TestClient(app)


def _default_bundle():
    """Return a ClimateDataBundle for a representative Indian location."""
    return load_climate_data(
        latitude=20.30,
        longitude=85.82,
        soil_ph=6.5,
        nitrogen=80.0,
        phosphorus=45.0,
        potassium=50.0,
    )


# ---------------------------------------------------------------------------
# climate_data_loader tests
# ---------------------------------------------------------------------------

class TestClimateDataLoader:

    def test_returns_ten_historical_years(self):
        bundle = _default_bundle()
        assert len(bundle.historical) == 10

    def test_historical_years_ascending(self):
        bundle = _default_bundle()
        years = [y.year for y in bundle.historical]
        assert years == sorted(years)

    def test_baseline_values_are_averages_of_last_five(self):
        bundle = _default_bundle()
        recent = bundle.historical[-5:]
        expected_temp = round(sum(y.avg_temperature for y in recent) / 5, 2)
        assert bundle.baseline_temp == expected_temp

    def test_climate_zone_is_non_empty_string(self):
        bundle = _default_bundle()
        assert isinstance(bundle.climate_zone, str)
        assert len(bundle.climate_zone) > 0

    def test_soil_profile_stored_correctly(self):
        bundle = _default_bundle()
        assert bundle.soil.ph == 6.5
        assert bundle.soil.nitrogen == 80.0

    def test_temp_trend_positive(self):
        """Global warming means temperature trend must be > 0."""
        bundle = _default_bundle()
        assert bundle.temp_trend_per_year > 0

    def test_cache_returns_same_object(self):
        """Two calls with the same rounded coordinates should hit the cache."""
        b1 = load_climate_data(20.30, 85.82, 6.5, 80, 45, 50)
        b2 = load_climate_data(20.30, 85.82, 6.8, 90, 40, 55)
        # Same object from cache (soil is updated in-place, lat/lon the same)
        assert b1 is b2

    def test_different_locations_differ(self):
        b_india  = load_climate_data(20.0, 85.0, 6.5, 80, 45, 50)
        b_europe = load_climate_data(51.5, 0.1,  7.0, 60, 30, 40)
        assert b_india.baseline_temp != b_europe.baseline_temp


# ---------------------------------------------------------------------------
# climate_prediction_model tests
# ---------------------------------------------------------------------------

class TestClimatePredictionModel:

    def test_returns_correct_number_of_years(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle, horizon_years=7)
        assert len(pred.predicted_years) == 7

    def test_predicted_years_are_sequential(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle, horizon_years=5)
        years = [y.year for y in pred.predicted_years]
        diffs = [years[i+1] - years[i] for i in range(len(years) - 1)]
        assert all(d == 1 for d in diffs)

    def test_confidence_score_between_0_and_1(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle, horizon_years=5)
        assert 0.0 <= pred.confidence_score <= 1.0

    def test_model_type_is_string(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle)
        assert isinstance(pred.model_type, str)
        assert pred.model_type in ("RandomForest", "LinearTrend")

    def test_temperature_values_physically_plausible(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle, horizon_years=10)
        for y in pred.predicted_years:
            assert -10 <= y.avg_temperature <= 55

    def test_rainfall_non_negative(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle)
        for y in pred.predicted_years:
            assert y.total_rainfall >= 0

    def test_horizon_clamped_to_10(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle, horizon_years=99)
        assert len(pred.predicted_years) == 10


# ---------------------------------------------------------------------------
# crop_recommendation_engine tests
# ---------------------------------------------------------------------------

class TestCropRecommendationEngine:

    def test_score_in_range_optimal_is_one(self):
        assert _score_in_range(25, 20, 30, 10, 40) == 1.0

    def test_score_in_range_outside_stress_is_zero(self):
        assert _score_in_range(50, 20, 30, 10, 40) == 0.0

    def test_score_in_range_between_optimal_and_stress(self):
        score = _score_in_range(35, 20, 30, 10, 40)
        assert 0.0 < score < 1.0

    def test_recommend_returns_correct_count(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle)
        result = recommend_crops(bundle, pred, top_n=5)
        assert len(result.recommended_crops) == 5

    def test_scores_descending(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle)
        result = recommend_crops(bundle, pred, top_n=5)
        scores = [c.resilience_score for c in result.recommended_crops]
        assert scores == sorted(scores, reverse=True)

    def test_scores_between_0_and_1(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle)
        result = recommend_crops(bundle, pred)
        for c in result.recommended_crops:
            assert 0.0 <= c.resilience_score <= 1.0

    def test_planting_season_non_empty(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle)
        result = recommend_crops(bundle, pred)
        for c in result.recommended_crops:
            assert len(c.planting_season) > 0

    def test_explanation_is_non_empty_string(self):
        bundle = _default_bundle()
        pred = predict_future_climate(bundle)
        result = recommend_crops(bundle, pred)
        assert isinstance(result.explanation, str)
        assert len(result.explanation) > 10

    def test_all_crops_in_suitability_db_are_known(self):
        expected = {
            "Millet", "Sorghum", "Pigeon Pea", "Groundnut", "Cotton",
            "Maize", "Rice", "Wheat", "Chickpea", "Lentil",
        }
        assert set(CROP_SUITABILITY.keys()) == expected

    def test_millet_scores_high_for_hot_dry_climate(self):
        """Millet should score highly when conditions are hot and dry."""
        millet = CROP_SUITABILITY["Millet"]
        score = _resilience_score(
            "Millet", millet,
            pred_temp=32.0, pred_rain=400.0, pred_hum=55.0,
            soil_ph=6.5, nitrogen=25, phosphorus=22, potassium=35,
        )
        assert score > 0.6

    def test_rice_scores_low_for_dry_climate(self):
        """Rice needs lots of water; it should score low for low-rainfall and low-humidity regions."""
        rice = CROP_SUITABILITY["Rice"]
        # Use conditions clearly outside rice's ranges: hot, dry, low humidity
        score = _resilience_score(
            "Rice", rice,
            pred_temp=38.0,   # Near rice stress_max=40°C
            pred_rain=300.0,  # Well below rice rain_min=1000mm
            pred_hum=35.0,    # Below rice humidity_min=60%, below stress threshold
            soil_ph=6.5, nitrogen=90, phosphorus=45, potassium=50,
        )
        assert score < 0.5


# ---------------------------------------------------------------------------
# HTTP API tests
# ---------------------------------------------------------------------------

class TestClimateApiRoutes:

    def test_predict_future_crops_success(self):
        client = _make_client()
        response = client.post("/api/predict/future-crops", json={
            "latitude": 20.2961,
            "longitude": 85.8245,
            "soil_ph": 6.5,
            "nitrogen": 80,
            "phosphorus": 45,
            "potassium": 50,
        })
        assert response.status_code == 200
        body = response.json()
        assert "recommended_crops" in body
        assert len(body["recommended_crops"]) == 5

    def test_response_has_required_fields(self):
        client = _make_client()
        response = client.post("/api/predict/future-crops", json={
            "latitude": 20.0, "longitude": 85.0,
        })
        assert response.status_code == 200
        body = response.json()
        assert "future_climate_summary" in body
        assert "explanation" in body
        assert "confidence_score" in body
        assert "model_type" in body
        assert "temperature_trend" in body
        assert "rainfall_trend" in body

    def test_each_crop_has_score_and_season(self):
        client = _make_client()
        response = client.post("/api/predict/future-crops", json={
            "latitude": 15.0, "longitude": 75.0,
        })
        assert response.status_code == 200
        for crop in response.json()["recommended_crops"]:
            assert "crop" in crop
            assert "resilience_score" in crop
            assert "planting_season" in crop
            assert 0.0 <= crop["resilience_score"] <= 1.0

    def test_climate_summary_has_change_strings(self):
        client = _make_client()
        response = client.post("/api/predict/future-crops", json={
            "latitude": 22.0, "longitude": 88.0,
        })
        assert response.status_code == 200
        summary = response.json()["future_climate_summary"]
        assert "temperature_change" in summary
        assert "rainfall_variation" in summary
        assert "humidity_change" in summary

    def test_invalid_latitude_returns_422(self):
        client = _make_client()
        response = client.post("/api/predict/future-crops", json={
            "latitude": 200.0, "longitude": 85.0,
        })
        assert response.status_code == 422

    def test_invalid_longitude_returns_422(self):
        client = _make_client()
        response = client.post("/api/predict/future-crops", json={
            "latitude": 20.0, "longitude": -999.0,
        })
        assert response.status_code == 422

    def test_list_supported_crops(self):
        client = _make_client()
        response = client.get("/api/predict/future-crops/crops")
        assert response.status_code == 200
        body = response.json()
        assert "crops" in body
        assert "total" in body
        assert body["total"] == len(CROP_SUITABILITY)

    def test_horizon_years_clamped(self):
        """horizon_years > 10 should be rejected with 422."""
        client = _make_client()
        response = client.post("/api/predict/future-crops", json={
            "latitude": 20.0, "longitude": 85.0,
            "horizon_years": 15,
        })
        assert response.status_code == 422

    def test_trend_data_length_matches_horizon(self):
        client = _make_client()
        response = client.post("/api/predict/future-crops", json={
            "latitude": 20.0, "longitude": 85.0,
            "horizon_years": 5,
        })
        assert response.status_code == 200
        body = response.json()
        assert len(body["temperature_trend"]) == 5
        assert len(body["rainfall_trend"]) == 5
