"""
Farmer Assistant Chatbot API routes.

Endpoints (prefix: /api/chatbot):
  POST   /message         – Send a message and get a response
  GET    /suggestions     – Get follow-up suggestions based on intent
  POST   /clear-history   – Clear conversation history
  GET    /history         – Retrieve conversation history
"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.engines import chatbot_service as engine

logger = logging.getLogger("chatbot_routes")

router = APIRouter()

# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class MessageRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User's message to the chatbot")
    location: Optional[str] = Field(None, description="User's location/state for context")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation continuity")


class MessageResponse(BaseModel):
    response: str = Field(..., description="Chatbot's text response")
    intent: str = Field(..., description="Detected intent of the user message")
    suggestions: List[str] = Field(default_factory=list, description="Follow-up suggestion buttons")
    data: Optional[Dict[str, Any]] = Field(None, description="Structured data accompanying the response")
    session_id: str = Field(..., description="Session ID for this conversation")
    crops: List[str] = Field(default_factory=list, description="Crops detected in the query")


class SuggestionsResponse(BaseModel):
    suggestions: List[str] = Field(..., description="List of suggested follow-up queries")
    intent: str = Field(..., description="The intent for which suggestions are returned")


class ClearHistoryResponse(BaseModel):
    success: bool = Field(..., description="Whether history was cleared successfully")
    session_id: str = Field(..., description="Session ID that was cleared")
    message: str = Field(..., description="Confirmation message")


class ConversationTurn(BaseModel):
    role: str = Field(..., description="Speaker role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO-8601 timestamp")


class HistoryResponse(BaseModel):
    session_id: str
    history: List[ConversationTurn]
    count: int


# ---------------------------------------------------------------------------
# Intent → suggestions mapping (used by GET /suggestions)
# ---------------------------------------------------------------------------

_INTENT_SUGGESTIONS: Dict[str, List[str]] = {
    "crop_recommendation": [
        "What should I grow in Odisha this season?",
        "Best Kharif crop for my region",
        "Recommend a profitable crop",
    ],
    "price_prediction": [
        "What is the price of rice?",
        "Show current market prices",
        "Price trend for wheat",
    ],
    "crop_comparison": [
        "Compare rice and wheat",
        "Compare cotton and soybean",
        "Which is more profitable: maize or millet?",
    ],
    "risk_analysis": [
        "What are the risks for cotton farming?",
        "How to prevent tomato blight?",
        "Profitability analysis for rice",
    ],
    "season_query": [
        "What crops grow in Kharif season?",
        "Best time to plant wheat",
        "Summer crop recommendations",
    ],
    "soil_query": [
        "Soil requirements for rice",
        "What pH does cotton need?",
        "Best soil type for vegetables",
    ],
    "fertilizer_query": [
        "NPK dose for wheat",
        "Best fertilizer for tomato",
        "Organic manure alternatives",
    ],
    "yield_query": [
        "Expected yield for maize",
        "How much can I earn from one hectare of rice?",
        "Yield comparison for Kharif crops",
    ],
    "general": [
        "What crop should I grow this month?",
        "Compare rice and wheat",
        "Check risks for cotton farming",
    ],
}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/message",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a message to the farmer assistant chatbot",
    description=(
        "Process a natural-language query from a farmer and return a structured "
        "response with agricultural advice, market data, and follow-up suggestions. "
        "The chatbot is fully standalone and does not require any external AI API."
    ),
)
def send_message(payload: MessageRequest) -> MessageResponse:
    """
    Send a user message and receive a chatbot response.

    The chatbot detects the intent (crop recommendation, price query,
    comparison, risk analysis, season query, etc.) and returns a
    context-aware agricultural response.
    """
    # Assign a session ID if not provided
    session_id = payload.session_id or str(uuid.uuid4())

    logger.info(
        "ChatBot message | session=%s intent=pending msg_len=%d loc=%s",
        session_id, len(payload.message), payload.location,
    )

    try:
        result = engine.process_query(
            message=payload.message,
            location=payload.location,
            user_id=payload.user_id,
            session_id=session_id,
        )
    except Exception as exc:
        logger.error("ChatBot engine error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your message. Please try again.",
        ) from exc

    logger.info(
        "ChatBot response | session=%s intent=%s crops=%s",
        session_id, result.get("intent"), result.get("crops"),
    )

    return MessageResponse(
        response=result["response"],
        intent=result["intent"],
        suggestions=result.get("suggestions", []),
        data=result.get("data"),
        session_id=result["session_id"],
        crops=result.get("crops", []),
    )


@router.get(
    "/suggestions",
    response_model=SuggestionsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get follow-up suggestions for a given intent",
    description="Return a list of suggested follow-up queries based on the detected or specified intent.",
)
def get_suggestions(
    intent: str = Query(
        default="general",
        description=(
            "Intent type to get suggestions for. Valid values: "
            "crop_recommendation, price_prediction, crop_comparison, "
            "risk_analysis, season_query, soil_query, fertilizer_query, "
            "yield_query, general"
        ),
    )
) -> SuggestionsResponse:
    """Return quick-reply suggestions for a specific intent type."""
    suggestions = _INTENT_SUGGESTIONS.get(intent, _INTENT_SUGGESTIONS["general"])
    return SuggestionsResponse(suggestions=suggestions, intent=intent)


@router.post(
    "/clear-history",
    response_model=ClearHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Clear conversation history for a session",
    description="Remove all stored conversation turns for the given session ID.",
)
def clear_history(
    session_id: str = Query(
        ...,
        description="The session ID whose history should be cleared",
    )
) -> ClearHistoryResponse:
    """Clear conversation history for the specified session."""
    engine.clear_history(session_id)
    logger.info("Conversation history cleared | session=%s", session_id)
    return ClearHistoryResponse(
        success=True,
        session_id=session_id,
        message=f"Conversation history cleared for session {session_id}.",
    )


@router.get(
    "/history",
    response_model=HistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get conversation history for a session",
    description="Retrieve the recent conversation turns for the given session ID.",
)
def get_history(
    session_id: str = Query(
        ...,
        description="The session ID to retrieve history for",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of conversation turns to return (1–50)",
    ),
) -> HistoryResponse:
    """Retrieve recent conversation history for the specified session."""
    raw_history = engine.get_history(session_id, limit=limit)
    turns = [
        ConversationTurn(
            role=turn["role"],
            content=turn["content"],
            timestamp=turn["timestamp"],
        )
        for turn in raw_history
    ]
    return HistoryResponse(
        session_id=session_id,
        history=turns,
        count=len(turns),
    )
