"""
Chatbot API endpoints:
  POST   /api/chat            – text chat
  GET    /api/chat/history/{session_id} – conversation history
  DELETE /api/chat/history/{session_id} – clear history
  GET    /api/chat/audio/{filename}     – serve TTS audio files
"""
import os
import tempfile
import uuid
from typing import List

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

from app.core.logger import api_logger as logger
from app.schemas.chatbot_schema import (
    ChatRequest,
    ChatResponse,
    ComparisonEntry,
    ConversationHistoryResponse,
    ConversationTurn,
    StructuredCropData,
)
from app.services import chatbot_service, conversation_memory
from app.utils.error_handler import ChatbotException
router = APIRouter()

# Directory where TTS audio files are stored (must match text_to_speech.py)
_AUDIO_DIR = os.path.join(tempfile.gettempdir(), "agripredict_tts")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_response(raw: dict, session_id: str) -> ChatResponse:
    """Convert the raw service dict to a ChatResponse schema."""
    sd_raw = raw.get("structured_data") or {}
    structured_data = StructuredCropData(**{
        k: v for k, v in sd_raw.items()
        if k in StructuredCropData.model_fields
    }) if sd_raw else None

    comp_raw = raw.get("comparison") or []
    comparison = [
        ComparisonEntry(**{k: v for k, v in c.items() if k in ComparisonEntry.model_fields})
        for c in comp_raw
    ] if comp_raw else None

    return ChatResponse(
        reply_text=raw.get("reply_text", ""),
        reply_audio_url=raw.get("reply_audio_url"),
        structured_data=structured_data,
        comparison=comparison,
        suggestions=raw.get("suggestions", []),
        detected_language=raw.get("detected_language", "en"),
        session_id=session_id,
        request_id=raw.get("request_id"),
        error=raw.get("error"),
        error_code=raw.get("error_code"),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

async def _chat_impl(request: Request) -> JSONResponse:
    """
    Process a text message from a farmer and return an AI-generated response.

    On unexpected errors the response includes an ``error_code`` and
    ``request_id`` so callers can correlate failures with server logs.
    """
    try:
        data = await request.json()
    except Exception as exc:
        logger.exception("Invalid JSON body for /api/chat: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"reply": "Invalid JSON request body.", "reply_text": "Invalid JSON request body."},
        )

    if not isinstance(data, dict):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"reply": "Invalid request body.", "reply_text": "Invalid request body."},
        )

    message = data.get("message")
    if not isinstance(message, str) or not message.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "reply": "Invalid input: 'message' is required.",
                "reply_text": "Invalid input: 'message' is required.",
            },
        )

    language = data.get("language")
    if not isinstance(language, str) or not language.strip():
        language = "en"

    session_raw = data.get("session_id")
    session_id = session_raw.strip() if isinstance(session_raw, str) and session_raw.strip() else str(uuid.uuid4())

    logger.info(
        "Chat request | session=%s lang=%s msg_len=%d",
        session_id, language, len(message.strip()),
    )
    logger.debug("Chat request body | session=%s msg='%.200s'", session_id, message)

    try:
        raw = chatbot_service.process_message(
            message=message.strip(),
            language=language,
            session_id=session_id,
        )

        if not isinstance(raw, dict):
            raw = {"reply_text": "Sorry, I could not generate a response right now."}

        normalized = _build_response(raw, session_id)
        payload = jsonable_encoder(normalized)
        reply_text = payload.get("reply_text") or ""
        payload["reply"] = str(reply_text)
        return JSONResponse(status_code=status.HTTP_200_OK, content=payload)
    except ChatbotException as exc:
        error_code = getattr(exc.error_code, "value", str(exc.error_code or "CHAT_001"))
        logger.exception(
            "ChatbotException [%s] %s: %s | details=%s",
            exc.request_id, error_code, exc.message, exc.details,
        )
        error_reply = "Sorry, I encountered an error processing your request. Please try again."
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "reply": error_reply,
                "reply_text": error_reply,
                "error": exc.message,
                "error_code": error_code,
            },
        )
    except Exception as exc:
        logger.exception("Unexpected chatbot processing error: %s", exc)
        error_reply = "Sorry, I encountered an unexpected error. Please try again."
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "reply": error_reply,
                "reply_text": error_reply,
                "error": "An unexpected error occurred.",
                "error_code": "UNK_001",
            },
        )


@router.post("", summary="Send a chat message")
async def chat_no_trailing_slash(request: Request) -> JSONResponse:
    """Handle /api/chat without redirect."""
    return await _chat_impl(request)


@router.post("/", summary="Send a chat message", include_in_schema=False)
async def chat_with_trailing_slash(request: Request) -> JSONResponse:
    """Handle /api/chat/ for compatibility with existing clients."""
    return await _chat_impl(request)


@router.get("/history/{session_id}", response_model=ConversationHistoryResponse)
def get_history(session_id: str) -> ConversationHistoryResponse:
    """Return the conversation history for a given session."""
    turns_raw = conversation_memory.get_history(session_id)
    turns = [ConversationTurn(**t) for t in turns_raw]
    return ConversationHistoryResponse(
        session_id=session_id,
        turns=turns,
        total_turns=len(turns),
    )


@router.delete(
    "/history/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear conversation history",
)
def clear_history(session_id: str) -> None:
    """Delete all conversation history for a session."""
    conversation_memory.clear_history(session_id)


@router.get("/audio/{filename}", summary="Serve a TTS audio file")
def serve_audio(filename: str) -> FileResponse:
    """Stream a previously generated TTS audio file."""
    # Sanitise filename to prevent path traversal (including symlink attacks)
    safe_name = os.path.basename(filename)
    if not safe_name or ".." in safe_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filename")

    audio_path = os.path.join(_AUDIO_DIR, safe_name)
    # Use realpath to resolve symlinks and verify the file is within the audio directory
    resolved = os.path.realpath(audio_path)
    if not resolved.startswith(os.path.realpath(_AUDIO_DIR) + os.sep):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filename")
    if not os.path.isfile(resolved):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio file not found")

    return FileResponse(resolved, media_type="audio/mpeg", filename=safe_name)
