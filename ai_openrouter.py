"""
Google Gemini API client with streaming support.
Primary AI engine for Gemini Virat Pro.
"""
import json
import requests
from config import GEMINI_API_KEY, GEMINI_API_URL, GEMINI_MODEL


def chat_gemini(messages: list, stream: bool = True) -> str:
    """Send messages to Gemini and return/stream the response."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set")

    # Convert OpenAI-style messages to Gemini format
    contents = []
    system_instruction = None

    for msg in messages:
        if msg["role"] == "system":
            system_instruction = msg["content"]
        else:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

    payload = {"contents": contents}
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    if stream:
        return _stream_gemini(payload)
    else:
        return _sync_gemini(payload)


def _stream_gemini(payload: dict) -> str:
    """Stream response token by token."""
    url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:streamGenerateContent?alt=sse&key={GEMINI_API_KEY}"

    resp = requests.post(url, json=payload, stream=True, timeout=120)
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
            text = data.get("candidates", [{}])[0] \
                       .get("content", {}) \
                       .get("parts", [{}])[0] \
                       .get("text", "")
            if text:
                print(text, end="", flush=True)
                full_text += text
        except (json.JSONDecodeError, IndexError, KeyError):
            continue

    print()  # newline after stream
    return full_text


def _sync_gemini(payload: dict) -> str:
    """Non-streaming request."""
    url = f"{GEMINI_API_URL}/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()

    data = resp.json()
    text = data.get("candidates", [{}])[0] \
               .get("content", {}) \
               .get("parts", [{}])[0] \
               .get("text", "")
    return text
