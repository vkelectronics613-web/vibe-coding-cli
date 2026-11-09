"""
Central configuration for Vibe Coding CLI.
Modular LLM provider settings and agent defaults.
"""
import os

# ─── API Keys ────────────────────────────────────────────
ANTHROPIC_API_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
GEMINI_API_KEY     = os.environ.get("GEMINI_API_KEY", "")
IMAGE_API_KEY      = os.environ.get("IMAGE_API_KEY", "")

# ─── Model Configuration ─────────────────────────────────
CLAUDE_MODEL       = "claude-3-5-sonnet-20241022"
OPENROUTER_MODEL   = "anthropic/claude-3.5-sonnet"
GEMINI_MODEL       = "gemini-2.0-flash"

# ─── API Endpoints ───────────────────────────────────────
ANTHROPIC_API_URL  = "https://api.anthropic.com/v1/messages"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
GEMINI_API_URL     = "https://generativelanguage.googleapis.com/v1beta/models"

# ─── Agent Settings ──────────────────────────────────────
MAX_AGENT_ITERATIONS = 10
CODE_TIMEOUT         = 30   # seconds

# ─── Memory ──────────────────────────────────────────────
MEMORY_SIZE = 50

# ─── System Prompts ──────────────────────────────────────
SYSTEM_PROMPT = """You are Vibe Coding Assistant, an elite autonomous developer CLI agent.
You provide clean, robust, and idiomatic code tailored for terminal-first developer workflows.

Your strengths:
- Expert-level engineering across modern programming languages
- Actionable, minimal, and precise answers
- Autonomous task execution with tool calling
- File operations, AST understanding, and safe code modification

Rules:
- Always deliver production-grade, tested solutions
- Follow modern design patterns and idiomatic practices
- When using tools, output TOOL_CALL: {"tool": "<name>", "args": {<args>}}
"""

AGENT_PROMPT = """You are an autonomous AI coding agent. Break the task into discrete steps and execute them.

Available tools:
- read_file(path): Read a file
- write_file(path, content): Write/create a file
- list_files(directory): List directory contents
- search_files(directory, pattern): Search files by pattern
- file_tree(directory, max_depth): Show directory tree
- run_python(code): Execute Python code (30s timeout)

To invoke a tool, output:
TOOL_CALL: {"tool": "<tool_name>", "args": {"param": "value"}}

After each tool result, evaluate the output and proceed to the next step.
When the task is finished, emit "TASK_COMPLETE" with a concise summary.
"""
