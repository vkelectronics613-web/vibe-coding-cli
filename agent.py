"""
AI Router — Gemini-first with automatic OpenRouter fallback.
Handles all AI requests with graceful degradation.
"""
from ai_gemini import chat_gemini
from ai_openrouter import chat_openrouter
from config import GEMINI_API_KEY, OPENROUTER_API_KEY


def route_chat(messages: list, stream: bool = True) -> str:
    """Route chat to the best available AI provider."""

    # Strategy 1: Try Gemini (primary)
    if GEMINI_API_KEY:
        try:
            return chat_gemini(messages, stream=stream)
        except Exception as e:
            print(f"  ⚠ Gemini unavailable ({_short_error(e)}), switching to fallback...")

    # Strategy 2: Try OpenRouter (fallback)
    if OPENROUTER_API_KEY:
        try:
            return chat_openrouter(messages, stream=stream)
        except Exception as e:
            print(f"  ✖ OpenRouter also failed: {_short_error(e)}")

    # No providers available
    return _no_provider_message()


def get_provider_status() -> dict:
    """Check which providers are configured."""
    return {
        "gemini": bool(GEMINI_API_KEY),
        "openrouter": bool(OPENROUTER_API_KEY),
    }


def _short_error(e: Exception) -> str:
    """Return a clean, short error description."""
    msg = str(e)
    if len(msg) > 80:
        msg = msg[:77] + "..."
    return msg


def _no_provider_message() -> str:
    msg = (
        "\n  ✖ No AI provider available.\n"
        "  Set at least one API key:\n"
        "    export GEMINI_API_KEY=\"your_key\"\n"
        "    export OPENROUTER_API_KEY=\"your_key\"\n"
    )
    print(msg)
    return ""
