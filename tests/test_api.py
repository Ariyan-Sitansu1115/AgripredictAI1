"""Focused API tests for stable chat behavior."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import chatbot_api


def _make_client() -> TestClient:
    app = FastAPI()
    app.include_router(chatbot_api.router, prefix="/api/chat")

    @app.get("/health")
    def health() -> dict:
        return {"status": "healthy"}

    return TestClient(app)


def test_health_check() -> None:
    """Health endpoint should respond with OK payload."""
    client = _make_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_invalid_json_returns_400() -> None:
    """Malformed JSON should not crash the route and must return 400."""
    client = _make_client()
    response = client.post(
        "/api/chat/",
        data='{"message": ',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    body = response.json()
    assert isinstance(body.get("reply"), str)
    assert isinstance(body.get("reply_text"), str)


def test_chat_missing_message_returns_400() -> None:
    """Missing/empty message should return validation error response."""
    client = _make_client()
    response = client.post("/api/chat/", json={"language": "en"})
    assert response.status_code == 400
    body = response.json()
    assert "reply" in body
    assert "message" in body["reply"].lower()


def test_chat_success_returns_reply_and_reply_text(monkeypatch) -> None:
    """Successful processing should return frontend-compatible fields."""

    def _fake_process_message(message: str, language: str, session_id: str) -> dict:
        return {
            "reply_text": f"echo: {message}",
            "reply_audio_url": None,
            "structured_data": None,
            "comparison": None,
            "suggestions": ["Try another crop"],
            "detected_language": language,
            "request_id": session_id,
        }

    monkeypatch.setattr(chatbot_api.chatbot_service, "process_message", _fake_process_message)

    client = _make_client()
    response = client.post("/api/chat/", json={"message": "hello", "language": "en"})
    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "echo: hello"
    assert body["reply_text"] == "echo: hello"
    assert isinstance(body.get("session_id"), str)


def test_chat_no_trailing_slash_no_redirect(monkeypatch) -> None:
    """Calling /api/chat should not rely on redirect and should return JSON directly."""

    def _fake_process_message(message: str, language: str, session_id: str) -> dict:
        return {
            "reply_text": f"echo: {message}",
            "detected_language": language,
            "request_id": session_id,
        }

    monkeypatch.setattr(chatbot_api.chatbot_service, "process_message", _fake_process_message)

    client = _make_client()
    response = client.post("/api/chat", json={"message": "hello", "language": "en"}, follow_redirects=False)
    assert response.status_code == 200
    assert "location" not in {k.lower(): v for k, v in response.headers.items()}
    body = response.json()
    assert body["reply"] == "echo: hello"


def test_chat_unexpected_error_returns_safe_200(monkeypatch) -> None:
    """Unexpected exceptions should be handled and returned as safe JSON payload."""

    def _raise_error(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(chatbot_api.chatbot_service, "process_message", _raise_error)

    client = _make_client()
    response = client.post("/api/chat/", json={"message": "hello", "language": "en"})
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get("reply"), str)
    assert isinstance(body.get("reply_text"), str)
    assert body.get("error_code") == "UNK_001"
