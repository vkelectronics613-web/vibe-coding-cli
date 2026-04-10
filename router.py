"""
OpenRouter API client with streaming support.
Fallback AI engine when Gemini is unavailable.
"""
import json
import requests
from config import OPENROUTER_API_KEY, OPENROUTER_API_URL, OPENROUTER_MODEL


def chat_openrouter(messages: list, stream: bool = True) -> str:
    """Send messages to OpenRouter and return/stream the response."""
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/geminiopenv-ai",
        "X-Title": "Gemini Virat Pro AI",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "stream": stream,
    }

    if stream:
        return _stream_openrouter(headers, payload)
    else:
        return _sync_openrouter(headers, payload)


def _stream_openrouter(headers: dict, payload: dict) -> str:
    """Stream response token by token."""
    resp = requests.post(
        OPENROUTER_API_URL, headers=headers, json=payload,
        stream=True, timeout=120
    )
    resp.raise_for_status()

    full_text = ""
    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        data_str = line[6:].strip()
        if data_str == "[DONE]":
            break
        try:
            data = json.loads(data_str)
            delta = data.get("choices", [{}])[0] \
                        .get("delta", {}) \
                        .get("content", "")
            if delta:
                print(delta, end="", flush=True)
                full_text += delta
        except (json.JSONDecodeError, IndexError, KeyError):
            continue

    print()
    return full_text


def _sync_openrouter(headers: dict, payload: dict) -> str:
    """Non-streaming request."""
    payload["stream"] = False
    resp = requests.post(
        OPENROUTER_API_URL, headers=headers, json=payload, timeout=120
    )
    resp.raise_for_status()

    data = resp.json()
    return data.get("choices", [{}])[0] \
               .get("message", {}) \
               .get("content", "")
