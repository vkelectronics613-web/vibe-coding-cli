"""
Central configuration for Gemini Virat Pro AI.
All settings in one place for easy customization.
"""
import os

# ─── API Keys ────────────────────────────────────────────
GEMINI_API_KEY     = os.environ.get("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
IMAGE_API_KEY      = os.environ.get("IMAGE_API_KEY", "")

# ─── Model Configuration ─────────────────────────────────
GEMINI_MODEL       = "gemini-2.0-flash"
OPENROUTER_MODEL   = "google/gemini-2.0-flash-exp:free"

# ─── API Endpoints ───────────────────────────────────────
GEMINI_API_URL     = "https://generativelanguage.googleapis.com/v1beta/models"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ─── Agent Settings ──────────────────────────────────────
MAX_AGENT_ITERATIONS = 10
CODE_TIMEOUT         = 30   # seconds

# ─── Memory ──────────────────────────────────────────────
MEMORY_SIZE = 50

# ─── System Prompts ──────────────────────────────────────
SYSTEM_PROMPT = """You are Gemini Virat Pro AI, an elite hybrid coding assistant.
You combine the best of ChatGPT, Gemini, and AutoGPT.

Your strengths:
- Expert-level coding in all languages
- Clear, concise, and actionable explanations
- Autonomous task execution with tool calling
- File system operations and code execution

Rules:
- Always provide working, production-ready code
- Use best practices and modern patterns
- Be concise but thorough
- When using tools, output TOOL_CALL: {"tool": "<name>", "args": {<args>}}
"""

AGENT_PROMPT = """You are an autonomous AI agent. Break the task into steps and execute them.

Available tools:
- read_file(path): Read a file
- write_file(path, content): Write/create a file
- list_files(directory): List directory contents
- search_files(directory, pattern): Search by pattern
- file_tree(directory, max_depth): Show directory tree
- run_python(code): Execute Python code (30s timeout)

To use a tool, output exactly:
TOOL_CALL: {"tool": "<tool_name>", "args": {"param": "value"}}

After each tool result, plan your next step.
When the task is complete, say "TASK_COMPLETE" and summarize what you did.
"""
