"""
Tests for the Farmer Assistant Chatbot (app/engines/chatbot_service.py and
app/api/chatbot_routes.py).
"""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.chatbot_routes import router
from app.engines.chatbot_service import FarmerAssistantChatbot, process_query


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def chatbot() -> FarmerAssistantChatbot:
    return FarmerAssistantChatbot()


@pytest.fixture(scope="module")
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# ---------------------------------------------------------------------------
# Chatbot Engine tests
# ---------------------------------------------------------------------------

class TestChatbotEngine:
    def test_knowledge_base_has_20_plus_crops(self, chatbot):
        assert len(chatbot._kb) >= 20

    def test_knowledge_base_crop_has_required_fields(self, chatbot):
        for crop, info in chatbot._kb.items():
            assert "season" in info, f"{crop} missing season"
            assert "rainfall_mm" in info, f"{crop} missing rainfall_mm"
            assert "temperature_c" in info, f"{crop} missing temperature_c"
            assert "soil_ph" in info, f"{crop} missing soil_ph"
            assert "fertilizer" in info, f"{crop} missing fertilizer"
            assert "yield_kg_ha" in info, f"{crop} missing yield_kg_ha"
            assert "regions" in info, f"{crop} missing regions"
            assert "profitability_score" in info, f"{crop} missing profitability_score"

    def test_market_prices_populated(self, chatbot):
        assert len(chatbot._prices) >= 10

    def test_intent_crop_recommendation(self, chatbot):
        result = chatbot.process_query("What should I grow this season?")
        assert result["intent"] == "crop_recommendation"

    def test_intent_price_prediction(self, chatbot):
        result = chatbot.process_query("What is the price of rice?")
        assert result["intent"] == "price_prediction"
        assert "rice" in result["response"].lower() or "Rice" in result["response"]

    def test_intent_crop_comparison(self, chatbot):
        result = chatbot.process_query("Compare rice and wheat")
        assert result["intent"] == "crop_comparison"

    def test_intent_risk_analysis(self, chatbot):
        result = chatbot.process_query("What are the risks for cotton farming?")
        assert result["intent"] == "risk_analysis"

    def test_intent_season_query(self, chatbot):
        result = chatbot.process_query("When is the best time to plant wheat?")
        assert result["intent"] == "season_query"

    def test_suggestions_returned(self, chatbot):
        result = chatbot.process_query("What crop should I grow?")
        assert isinstance(result["suggestions"], list)
        assert len(result["suggestions"]) > 0

    def test_response_is_non_empty_string(self, chatbot):
        result = chatbot.process_query("Tell me about rice farming")
        assert isinstance(result["response"], str)
        assert len(result["response"]) > 0

    def test_session_id_assigned(self, chatbot):
        result = chatbot.process_query("Hello")
        assert isinstance(result["session_id"], str)
        assert len(result["session_id"]) > 0

    def test_session_id_preserved(self, chatbot):
        sid = "test-session-123"
        result = chatbot.process_query("Hello", session_id=sid)
        assert result["session_id"] == sid

    def test_location_context_used(self, chatbot):
        result = chatbot.process_query("best crop", location="Odisha")
        assert result["intent"] == "crop_recommendation"

    def test_crop_extraction_rice(self, chatbot):
        result = chatbot.process_query("Tell me about rice cultivation")
        assert "Rice" in result.get("crops", [])

    def test_crop_extraction_cotton(self, chatbot):
        result = chatbot.process_query("risks for cotton farming")
        assert "Cotton" in result.get("crops", [])

    def test_price_response_contains_price(self, chatbot):
        result = chatbot.process_query("What is the price of wheat?")
        assert "₹" in result["response"] or "price" in result["response"].lower()

    def test_comparison_includes_both_crops(self, chatbot):
        result = chatbot.process_query("Compare rice and maize")
        assert "Rice" in result["response"]
        assert "Maize" in result["response"]

    def test_risk_analysis_includes_risk_level(self, chatbot):
        result = chatbot.process_query("Analyze risk for tomato")
        assert result.get("data") is not None
        assert "risk_level" in result["data"]

    def test_general_query_fallback(self, chatbot):
        result = chatbot.process_query("xyzabc random text 12345")
        assert result["intent"] == "general"
        assert isinstance(result["response"], str)
        assert len(result["response"]) > 0

    def test_module_level_process_query(self):
        result = process_query("What should I grow in Odisha?", location="Odisha")
        assert result["intent"] == "crop_recommendation"
        assert isinstance(result["suggestions"], list)


class TestConversationHistory:
    def test_history_is_stored(self, chatbot):
        from app.engines.chatbot_service import get_history, clear_history
        sid = "history-test-session"
        chatbot.process_query("Hello", session_id=sid)
        history = get_history(sid)
        assert len(history) >= 1

    def test_clear_history(self, chatbot):
        from app.engines.chatbot_service import get_history, clear_history
        sid = "clear-test-session"
        chatbot.process_query("Hello", session_id=sid)
        clear_history(sid)
        history = get_history(sid)
        assert len(history) == 0

    def test_history_limit(self, chatbot):
        from app.engines.chatbot_service import get_history
        sid = "limit-test-session"
        for _ in range(5):
            chatbot.process_query("Price of rice?", session_id=sid)
        history = get_history(sid, limit=3)
        assert len(history) <= 3


# ---------------------------------------------------------------------------
# API Route tests
# ---------------------------------------------------------------------------

class TestChatbotMessageEndpoint:
    def test_post_message_returns_200(self, client):
        r = client.post("/message", json={"message": "What crop should I grow?"})
        assert r.status_code == 200

    def test_post_message_has_required_fields(self, client):
        r = client.post("/message", json={"message": "Compare rice and wheat"})
        body = r.json()
        assert "response" in body
        assert "intent" in body
        assert "suggestions" in body
        assert "session_id" in body

    def test_post_message_with_location(self, client):
        r = client.post("/message", json={
            "message": "What crop is best for me?",
            "location": "Odisha"
        })
        assert r.status_code == 200
        body = r.json()
        assert body["intent"] == "crop_recommendation"

    def test_post_message_missing_message_returns_422(self, client):
        r = client.post("/message", json={"location": "Odisha"})
        assert r.status_code == 422

    def test_post_message_empty_message_returns_422(self, client):
        r = client.post("/message", json={"message": ""})
        assert r.status_code == 422

    def test_post_message_session_preserved(self, client):
        sid = "api-test-session"
        r = client.post("/message", json={"message": "Hello", "session_id": sid})
        assert r.json()["session_id"] == sid

    def test_post_message_suggestions_are_list(self, client):
        r = client.post("/message", json={"message": "Price of cotton?"})
        body = r.json()
        assert isinstance(body["suggestions"], list)


class TestChatbotSuggestionsEndpoint:
    def test_get_suggestions_returns_200(self, client):
        r = client.get("/suggestions?intent=crop_recommendation")
        assert r.status_code == 200

    def test_get_suggestions_has_suggestions_field(self, client):
        r = client.get("/suggestions?intent=price_prediction")
        body = r.json()
        assert "suggestions" in body
        assert isinstance(body["suggestions"], list)
        assert len(body["suggestions"]) > 0

    def test_get_suggestions_intent_echoed(self, client):
        r = client.get("/suggestions?intent=risk_analysis")
        assert r.json()["intent"] == "risk_analysis"

    def test_get_suggestions_unknown_intent_returns_defaults(self, client):
        r = client.get("/suggestions?intent=unknown_xyz")
        assert r.status_code == 200
        assert len(r.json()["suggestions"]) > 0

    def test_get_suggestions_default_intent(self, client):
        r = client.get("/suggestions")
        assert r.status_code == 200


class TestChatbotClearHistoryEndpoint:
    def test_clear_history_returns_200(self, client):
        r = client.post("/clear-history?session_id=test-clear-session")
        assert r.status_code == 200

    def test_clear_history_success_true(self, client):
        r = client.post("/clear-history?session_id=test-clear-session-2")
        assert r.json()["success"] is True

    def test_clear_history_requires_session_id(self, client):
        r = client.post("/clear-history")
        assert r.status_code == 422


class TestChatbotHistoryEndpoint:
    def test_get_history_returns_200(self, client):
        r = client.get("/history?session_id=test-history-session")
        assert r.status_code == 200

    def test_get_history_has_required_fields(self, client):
        r = client.get("/history?session_id=test-history-session")
        body = r.json()
        assert "session_id" in body
        assert "history" in body
        assert "count" in body

    def test_get_history_empty_for_new_session(self, client):
        r = client.get("/history?session_id=brand-new-session-xyz-123")
        assert r.json()["count"] == 0

    def test_get_history_requires_session_id(self, client):
        r = client.get("/history")
        assert r.status_code == 422

    def test_get_history_limit_respected(self, client):
        r = client.get("/history?session_id=test-session&limit=5")
        assert r.status_code == 200
        assert r.json()["count"] <= 5
