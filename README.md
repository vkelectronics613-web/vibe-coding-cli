# ⚡ vibe-coding-cli

> An intelligent, extensible AI-assisted coding CLI agent featuring multi-model routing, session memory, and autonomous task execution.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org)

**vibe-coding-cli** streamlines developer workflows by integrating multiple LLM providers into a fast, terminal-first developer experience. It features session-specific memory, project context understanding, and dynamic routing across models.

---

## ✨ Features

- **Multi-Provider Routing:** Seamless routing between Gemini, OpenRouter, and custom endpoints.
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

Set your preferred LLM API keys:

```bash
export GEMINI_API_KEY="your_api_key_here"
export OPENROUTER_API_KEY="your_api_key_here"
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
├── agent.py           # Core agent logic and tool dispatch
├── router.py          # Dynamic LLM routing and dispatch
├── memory.py          # State, history, and context tracking
├── ai_gemini.py       # Google Gemini provider adapter
├── ai_openrouter.py   # OpenRouter multi-model provider adapter
└── LICENSE            # MIT License
```

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome. Please open an issue or submit a pull request!

## 📄 License

Distributed under the [MIT License](LICENSE).
