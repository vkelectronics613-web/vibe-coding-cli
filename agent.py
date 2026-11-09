"""
AI Router — Claude & OpenRouter first with multi-provider fallbacks.
Handles all AI coding requests with graceful degradation.
"""
from ai_claude import ClaudeProvider
from ai_openrouter import chat_openrouter
from memory import ANTHROPIC_API_KEY, OPENROUTER_API_KEY, GEMINI_API_KEY

_claude = ClaudeProvider()


def route_chat(messages: list, stream: bool = True) -> str:
    """Route chat to the best available AI provider."""

    # Strategy 1: Try Anthropic Claude (primary)
    if ANTHROPIC_API_KEY and _claude.is_available():
        try:
            last_msg = messages[-1]["content"] if messages else ""
            return _claude.generate(last_msg)
        except Exception as e:
            print(f"  ⚠ Claude unavailable ({_short_error(e)}), switching to fallback...")

    # Strategy 2: Try OpenRouter (Claude 3.5 Sonnet / Multi-model)
    if OPENROUTER_API_KEY:
        try:
            return chat_openrouter(messages, stream=stream)
        except Exception as e:
            print(f"  ⚠ OpenRouter fallback failed: {_short_error(e)}")

    # Strategy 3: Try Gemini (optional fallback)
    if GEMINI_API_KEY:
        try:
            from ai_gemini import chat_gemini
            return chat_gemini(messages, stream=stream)
        except Exception as e:
            print(f"  ⚠ Gemini also failed: {_short_error(e)}")

    # No providers available
    return _no_provider_message()


def get_provider_status() -> dict:
    """Check which providers are configured."""
    return {
        "claude": bool(ANTHROPIC_API_KEY),
        "openrouter": bool(OPENROUTER_API_KEY),
        "gemini": bool(GEMINI_API_KEY),
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
        "    export ANTHROPIC_API_KEY=\"your_key\"   # Recommended (Claude 3.5 Sonnet)\n"
        "    export OPENROUTER_API_KEY=\"your_key\"\n"
        "    export GEMINI_API_KEY=\"your_key\"\n"
    )
    print(msg)
    return ""
