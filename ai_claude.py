import os
import json
from typing import Dict, Any, Optional

class ClaudeProvider:
    """
    Anthropic Claude Provider implementation for vibe-coding-cli.
    Enables native Claude 3.5 Sonnet / Haiku integration and tool calling.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = None

        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                self.client = None

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("ANTHROPIC_API_KEY environment variable is not configured.")

        if not self.client:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system or "You are an autonomous expert software engineering agent in a terminal-first workflow.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
