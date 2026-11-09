# ⚡ vibe-coding-cli

> An intelligent, extensible AI-assisted coding CLI agent featuring multi-model routing (Claude 3.5 Sonnet, OpenRouter), session memory, and autonomous task execution.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org)
[![Anthropic Claude](https://img.shields.io/badge/Anthropic-Claude_3.5_Sonnet-D97706.svg)](https://anthropic.com)

**vibe-coding-cli** streamlines developer workflows by integrating LLM providers (Anthropic Claude, OpenRouter) into a fast, terminal-first developer experience. It features session-specific memory, project context understanding, and dynamic routing across models.

---

## ✨ Features

- **Claude 3.5 Sonnet Integration:** First-class support for Anthropic Claude reasoning and code generation.
- **Multi-Provider Fallbacks:** Flexible routing across Anthropic, OpenRouter, and custom endpoints.
- **Context & Session Memory:** Retains multi-turn conversation and project context during active sessions.
- **Terminal-First Workflow:** Lightweight REPL designed for rapid iteration directly from your command line.
- **Extensible Agents:** Modular agent structure for adding new tool calls, generation tasks, and code diffing.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/vkelectronics613-web/vibe-coding-cli.git
cd vibe-coding-cli

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### Environment Setup

Set your preferred LLM API key (Claude 3.5 Sonnet recommended):

```bash
export ANTHROPIC_API_KEY="your_anthropic_api_key"
# Optional Fallback:
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

### Usage

```bash
python main.py
```

---

## 📂 Architecture & Project Structure

```text
vibe-coding-cli/
├── main.py            # CLI entrypoint and interactive loop
├── agent.py           # Core agent logic and dynamic provider routing
├── ai_claude.py       # Anthropic Claude 3.5 Sonnet provider adapter
├── ai_openrouter.py   # OpenRouter multi-model provider adapter
├── router.py          # Provider client routines and streaming handlers
├── memory.py          # State, history, and context tracking
├── CONTRIBUTING.md    # Contribution guidelines
└── LICENSE            # MIT License
```

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

Distributed under the [MIT License](LICENSE).
