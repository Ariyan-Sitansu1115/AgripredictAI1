"""
Tests for Climate-Resilient Crop Recommendation Engine API.

All tests run in-process using FastAPI's TestClient – no external services
or database required.
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import climate_routes


# ---------------------------------------------------------------------------
# Test app / client fixture
# ---------------------------------------------------------------------------

def _make_client() -> TestClient:
    app = FastAPI()
    app.include_router(climate_routes.router, prefix="/api/climate")
    return TestClient(app)


@pytest.fixture()
def client() -> TestClient:
    return _make_client()


# ---------------------------------------------------------------------------
# Shared payloads
# ---------------------------------------------------------------------------

VALID_PAYLOAD = {
    "latitude": 20.2961,
    "longitude": 85.8245,
    "soil_ph": 6.5,
    "nitrogen": 80.0,
    "phosphorus": 45.0,
    "potassium": 50.0,
    "target_year": 2035,
    "top_n": 5,
}


# ---------------------------------------------------------------------------
# POST /api/climate/predict/future-crops
# ---------------------------------------------------------------------------

class TestPredictFutureCrops:
    def test_returns_200_with_valid_payload(self, client):
        resp = client.post("/api/climate/predict/future-crops", json=VALID_PAYLOAD)
        assert resp.status_code == 200

    def test_recommended_crops_list_not_empty(self, client):
        resp = client.post("/api/climate/predict/future-crops", json=VALID_PAYLOAD)
        data = resp.json()
        assert "recommended_crops" in data
        assert len(data["recommended_crops"]) > 0

    def test_recommended_crops_count_respects_top_n(self, client):
        payload = {**VALID_PAYLOAD, "top_n": 3}
        resp = client.post("/api/climate/predict/future-crops", json=payload)
        data = resp.json()
        assert len(data["recommended_crops"]) <= 3

    def test_each_crop_has_required_fields(self, client):
        resp = client.post("/api/climate/predict/future-crops", json=VALID_PAYLOAD)
        for crop in resp.json()["recommended_crops"]:
            assert "crop" in crop
            assert "resilience_score" in crop
            assert "planting_season" in crop
            assert "expected_yield" in crop

    def test_resilience_scores_in_range(self, client):
        resp = client.post("/api/climate/predict/future-crops", json=VALID_PAYLOAD)
        for crop in resp.json()["recommended_crops"]:
            assert 0.0 <= crop["resilience_score"] <= 1.0

    def test_future_climate_summary_present(self, client):
        resp = client.post("/api/climate/predict/future-crops", json=VALID_PAYLOAD)
        summary = resp.json()["future_climate_summary"]
        assert "temperature_change" in summary
        assert "rainfall_variation" in summary
        assert "climate_zone" in summary
        assert "confidence_score" in summary

    def test_confidence_score_in_range(self, client):
        resp = client.post("/api/climate/predict/future-crops", json=VALID_PAYLOAD)
        score = resp.json()["future_climate_summary"]["confidence_score"]
        assert 0.0 <= score <= 1.0

    def test_explanation_is_non_empty_string(self, client):
        resp = client.post("/api/climate/predict/future-crops", json=VALID_PAYLOAD)
        explanation = resp.json().get("explanation", "")
        assert isinstance(explanation, str)
        assert len(explanation) > 10

    def test_climate_trends_present(self, client):
        resp = client.post("/api/climate/predict/future-crops", json=VALID_PAYLOAD)
        trends = resp.json().get("climate_trends", {})
        assert "temperature_trend" in trends
        assert "rainfall_trend" in trends
        assert len(trends["temperature_trend"]) > 0

    def test_invalid_latitude_returns_422(self, client):
        bad = {**VALID_PAYLOAD, "latitude": 200.0}
        resp = client.post("/api/climate/predict/future-crops", json=bad)
        assert resp.status_code == 422

    def test_invalid_longitude_returns_422(self, client):
        bad = {**VALID_PAYLOAD, "longitude": -200.0}
        resp = client.post("/api/climate/predict/future-crops", json=bad)
        assert resp.status_code == 422

    def test_invalid_target_year_returns_422(self, client):
        bad = {**VALID_PAYLOAD, "target_year": 2020}  # before 2025
        resp = client.post("/api/climate/predict/future-crops", json=bad)
        assert resp.status_code == 422

    def test_missing_required_fields_returns_422(self, client):
        resp = client.post("/api/climate/predict/future-crops", json={})
        assert resp.status_code == 422

    def test_default_soil_values_accepted(self, client):
        minimal = {"latitude": 20.2961, "longitude": 85.8245}
        resp = client.post("/api/climate/predict/future-crops", json=minimal)
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# GET /api/climate/trends/{lat}/{lon}
# ---------------------------------------------------------------------------

class TestGetClimateTrends:
    def test_returns_200(self, client):
        resp = client.get("/api/climate/trends/20.2961/85.8245")
        assert resp.status_code == 200

    def test_response_has_required_keys(self, client):
        resp = client.get("/api/climate/trends/20.2961/85.8245")
        data = resp.json()
        for key in ["latitude", "longitude", "historical_temp_avg",
                    "historical_rainfall_avg", "climate_zone",
                    "temperature_trend", "rainfall_trend"]:
            assert key in data

    def test_temperature_trend_is_list(self, client):
        resp = client.get("/api/climate/trends/20.2961/85.8245")
        assert isinstance(resp.json()["temperature_trend"], list)

    def test_rainfall_trend_is_list(self, client):
        resp = client.get("/api/climate/trends/20.2961/85.8245")
        assert isinstance(resp.json()["rainfall_trend"], list)

    def test_invalid_lat_returns_422(self, client):
        resp = client.get("/api/climate/trends/999/85.8245")
        assert resp.status_code == 422

    def test_invalid_lon_returns_422(self, client):
        resp = client.get("/api/climate/trends/20.2961/500")
        assert resp.status_code == 422

    def test_southern_hemisphere_location(self, client):
        resp = client.get("/api/climate/trends/-23.5/28.0")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST /api/climate/crop-adaptability
# ---------------------------------------------------------------------------

class TestCropAdaptability:
    ADAPT_PAYLOAD = {
        "crop_name": "Millet",
        "latitude": 20.2961,
        "longitude": 85.8245,
        "soil_ph": 6.5,
        "nitrogen": 80.0,
        "phosphorus": 45.0,
        "potassium": 50.0,
        "target_year": 2035,
    }

    def test_returns_200_for_known_crop(self, client):
        resp = client.post("/api/climate/crop-adaptability", json=self.ADAPT_PAYLOAD)
        assert resp.status_code == 200

    def test_response_has_required_fields(self, client):
        resp = client.post("/api/climate/crop-adaptability", json=self.ADAPT_PAYLOAD)
        data = resp.json()
        for key in ["crop", "current_suitability", "future_suitability",
                    "suitability_change", "adaptability_trend", "is_climate_resilient"]:
            assert key in data

    def test_adaptability_trend_valid_value(self, client):
        resp = client.post("/api/climate/crop-adaptability", json=self.ADAPT_PAYLOAD)
        trend = resp.json()["adaptability_trend"]
        assert trend in ("improving", "declining", "stable")

    def test_suitability_scores_in_range(self, client):
        resp = client.post("/api/climate/crop-adaptability", json=self.ADAPT_PAYLOAD)
        data = resp.json()
        assert 0.0 <= data["current_suitability"] <= 1.0
        assert 0.0 <= data["future_suitability"] <= 1.0

    def test_is_climate_resilient_is_bool(self, client):
        resp = client.post("/api/climate/crop-adaptability", json=self.ADAPT_PAYLOAD)
        assert isinstance(resp.json()["is_climate_resilient"], bool)

    def test_unknown_crop_returns_404(self, client):
        bad = {**self.ADAPT_PAYLOAD, "crop_name": "NonExistentCrop12345"}
        resp = client.post("/api/climate/crop-adaptability", json=bad)
        assert resp.status_code == 404

    def test_rice_adaptability(self, client):
        payload = {**self.ADAPT_PAYLOAD, "crop_name": "Rice"}
        resp = client.post("/api/climate/crop-adaptability", json=payload)
        assert resp.status_code == 200
        assert resp.json()["crop"] == "Rice"


# ---------------------------------------------------------------------------
# Unit tests for engine components
# ---------------------------------------------------------------------------

class TestClimateDataLoader:
    def test_load_historical_data_shape(self):
        from app.engines.climate_data_loader import ClimateDataLoader
        loader = ClimateDataLoader()
        data = loader.load_historical_climate_data(20.0, 85.0)
        assert len(data["temperature_monthly"]) == 360
        assert len(data["rainfall_monthly"]) == 360
        assert len(data["humidity_monthly"]) == 360

    def test_historical_temp_avg_realistic(self):
        from app.engines.climate_data_loader import ClimateDataLoader
        loader = ClimateDataLoader()
        data = loader.load_historical_climate_data(20.0, 85.0)
        # Should be a plausible temperature (not 0 or 100)
        assert 0 < data["temp_avg"] < 50

    def test_rainfall_avg_realistic(self):
        from app.engines.climate_data_loader import ClimateDataLoader
        loader = ClimateDataLoader()
        data = loader.load_historical_climate_data(20.0, 85.0)
        # Monthly rainfall avg should be plausible (0-500mm/month)
        assert 0 <= data["rainfall_avg"] <= 500

    def test_climate_zone_tropical(self):
        from app.engines.climate_data_loader import ClimateDataLoader
        loader = ClimateDataLoader()
        zone = loader.get_climate_zone(5.0, 26.0, 180.0)
        assert zone == "tropical"

    def test_climate_zone_arid(self):
        from app.engines.climate_data_loader import ClimateDataLoader
        loader = ClimateDataLoader()
        zone = loader.get_climate_zone(20.0, 30.0, 10.0)
        assert zone == "arid"


class TestCropSuitabilityMatcher:
    def test_crop_database_size(self):
        from app.engines.crop_suitability_matcher import CROP_DATABASE
        assert len(CROP_DATABASE) >= 30

    def test_score_between_zero_and_one(self):
        from app.engines.crop_suitability_matcher import CropSuitabilityMatcher
        matcher = CropSuitabilityMatcher()
        result = matcher.compute_suitability_score("Millet", 28.0, 70.0, 6.5, 80, 45, 50)
        assert 0.0 <= result["score"] <= 1.0

    def test_unknown_crop_returns_zero(self):
        from app.engines.crop_suitability_matcher import CropSuitabilityMatcher
        matcher = CropSuitabilityMatcher()
        result = matcher.compute_suitability_score("FakeCrop", 28.0, 70.0, 6.5, 80, 45, 50)
        assert result["score"] == 0.0

    def test_get_top_crops_returns_list(self):
        from app.engines.crop_suitability_matcher import CropSuitabilityMatcher
        matcher = CropSuitabilityMatcher()
        crops = matcher.get_top_crops(28.0, 70.0, 6.5, 80, 45, 50)
        assert isinstance(crops, list)

    def test_get_top_crops_respects_top_n(self):
        from app.engines.crop_suitability_matcher import CropSuitabilityMatcher
        matcher = CropSuitabilityMatcher()
        crops = matcher.get_top_crops(28.0, 70.0, 6.5, 80, 45, 50, top_n=3)
        assert len(crops) <= 3

    def test_crops_ordered_by_score_descending(self):
        from app.engines.crop_suitability_matcher import CropSuitabilityMatcher
        matcher = CropSuitabilityMatcher()
        crops = matcher.get_top_crops(28.0, 70.0, 6.5, 80, 45, 50, top_n=5)
        scores = [c["resilience_score"] for c in crops]
        assert scores == sorted(scores, reverse=True)
