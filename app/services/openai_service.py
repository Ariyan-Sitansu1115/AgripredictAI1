"""
OpenAI Service – wraps the OpenAI Chat Completions API for AgriPredictAI.

Provides:
  * ``extract_intent``    – parse crops / state / intent from a user message.
  * ``generate_response`` – produce a farmer-friendly reply from structured data.
  * ``get_chat_response`` – single call that returns a free-form reply (fallback).
"""
import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy OpenAI client (avoids import errors when the package is absent)
# ---------------------------------------------------------------------------

_client = None


def _get_client():
    """Return (and lazily initialise) the OpenAI client."""
    global _client
    if _client is None:
        try:
            from openai import OpenAI  # type: ignore
        except ImportError as exc:
            raise ImportError(
                "The 'openai' package is required. Install it with: pip install openai"
            ) from exc

        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Add it to your .env file."
            )
        _client = OpenAI(api_key=api_key)
    return _client


def _model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4-turbo")


# ---------------------------------------------------------------------------
# System prompt – agricultural context
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are AgriBot, an intelligent AI assistant built into the AgriPredict AI dashboard \
for Indian farmers and agricultural advisors.

Your role is to help farmers make data-driven decisions about:
- Crop price predictions and market trends
- Crop comparison and selection for a region/season
- Risk and profitability analysis
- Seasonal recommendations

Guidelines:
- Respond in a friendly, concise, and practical manner.
- Use ₹ for Indian Rupee and per-quintal pricing where relevant.
- When you have structured data (prices, risk levels, profitability scores) provided in the context, \
  include the key numbers in your reply.
- If no structured data is provided, use your agricultural knowledge for a helpful answer.
- Keep replies focused and under 200 words unless a detailed explanation is explicitly requested.
- Use emojis sparingly (🌾 💰 📈 ⚠️) to highlight key points.
- Supported crops: Rice, Wheat, Maize, Cotton, Sugarcane, Potato, Onion, Tomato, Cabbage, Carrot.
- Supported Indian states context is relevant for regional advice."""

_INTENT_EXTRACTION_PROMPT = """You are an entity extractor for an agricultural chatbot. \
Given a farmer's query (in English), extract the following fields and return ONLY valid JSON.

Fields:
- "intent_type": one of ["greeting","price_query","comparison","recommendation","risk_query","what_if","general"]
- "crops": list of crop names found (from: Rice, Wheat, Maize, Cotton, Sugarcane, Potato, Onion, Tomato, Cabbage, Carrot)
- "state": Indian state name if mentioned, else null
- "season": season if mentioned (e.g. "Rabi", "Kharif", "Zaid"), else null

Rules:
- "greeting" → hello/hi/hey/namaste queries
- "price_query" → asks about price, rate, cost, market value
- "comparison" → compares two or more crops or asks which is better
- "recommendation" → asks what to grow / best crop
- "risk_query" → asks about risk, danger, loss
- "what_if" → hypothetical scenario (what if I grow / should I plant)
- "general" → anything else

Return only the JSON object, no explanation."""


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def extract_intent(message: str) -> Dict[str, Any]:
    """
    Use OpenAI to extract intent and entities from *message*.

    Returns a dict with keys: intent_type, crops, state, season, raw_text.
    Falls back to a 'general' intent dict on any failure.
    """
    default = {
        "intent_type": "general",
        "crops": [],
        "state": None,
        "season": None,
        "raw_text": message,
    }

    try:
        client = _get_client()
        kwargs: Dict[str, Any] = dict(
            model=_model(),
            messages=[
                {"role": "system", "content": _INTENT_EXTRACTION_PROMPT},
                {"role": "user", "content": message},
            ],
            max_tokens=200,
            temperature=0,
        )
        # response_format=json_object requires gpt-4-turbo / gpt-3.5-turbo-1106+
        # Attempt it first; fall back gracefully if the model doesn't support it.
        try:
            kwargs["response_format"] = {"type": "json_object"}
            response = client.chat.completions.create(**kwargs)
        except Exception:
            kwargs.pop("response_format", None)
            response = client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content or "{}"
        parsed = json.loads(content)

        # Normalise / validate fields
        intent_type = str(parsed.get("intent_type", "general"))
        crops_raw = parsed.get("crops") or []
        crops = [c for c in crops_raw if isinstance(c, str)]
        state = parsed.get("state") or None
        season = parsed.get("season") or None

        logger.debug("OpenAI intent: type=%s crops=%s state=%s", intent_type, crops, state)
        return {
            "intent_type": intent_type,
            "crops": crops,
            "state": state,
            "season": season,
            "raw_text": message,
        }

    except Exception as exc:
        logger.warning("OpenAI intent extraction failed: %s – using fallback", exc)
        return {**default, "raw_text": message}


def generate_response(
    user_message: str,
    history: List[Dict[str, str]],
    data_context: Optional[str] = None,
) -> str:
    """
    Generate a conversational reply using GPT.

    Args:
        user_message:  The current user query (in English).
        history:       Previous conversation turns as [{role, content}, ...].
                       Automatically trimmed to the last 10 turns to stay within
                       token limits.
        data_context:  Optional structured data summary injected into the system
                       prompt so GPT can cite real numbers.

    Returns:
        The assistant reply string.

    Raises:
        Exception: Re-raises any OpenAI API error so callers can handle it.
    """
    system_content = _SYSTEM_PROMPT
    if data_context:
        system_content += f"\n\n--- Current data context ---\n{data_context}"

    # Limit history to the most recent 10 turns to avoid exceeding token limits
    trimmed_history = history[-10:] if len(history) > 10 else history

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_content}]
    messages.extend(trimmed_history)
    messages.append({"role": "user", "content": user_message})

    client = _get_client()
    try:
        response = client.chat.completions.create(
            model=_model(),
            messages=messages,
            max_tokens=400,
            temperature=0.7,
        )
        reply = (response.choices[0].message.content or "").strip()
        logger.debug("OpenAI response (%d chars)", len(reply))
        return reply
    except Exception as exc:
        logger.error("OpenAI generate_response failed: %s", exc)
        raise
