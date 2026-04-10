"""
Conversation memory with sliding window.
Stores the last N messages for context continuity.
"""
from collections import deque
from config import MEMORY_SIZE


class Memory:
    def __init__(self, max_size: int = MEMORY_SIZE):
        self._messages: deque = deque(maxlen=max_size)

    def add(self, role: str, content: str) -> None:
        """Add a message to memory."""
        self._messages.append({"role": role, "content": content})

    def get_messages(self) -> list:
        """Return all stored messages as a list."""
        return list(self._messages)

    def clear(self) -> None:
        """Clear all memory."""
        self._messages.clear()

    def display(self) -> str:
        """Format memory for display."""
        if not self._messages:
            return "  (no conversation history)"
        lines = []
        for i, msg in enumerate(self._messages, 1):
            role = "You" if msg["role"] == "user" else "AI"
            preview = msg["content"][:80].replace("\n", " ")
            if len(msg["content"]) > 80:
                preview += "..."
            lines.append(f"  {i:3d}. [{role}] {preview}")
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self._messages)
