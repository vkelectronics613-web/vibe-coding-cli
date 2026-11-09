# Contributing to vibe-coding-cli

Thank you for your interest in contributing to **vibe-coding-cli**! We welcome bug fixes, documentation improvements, new model provider adapters, and Model Context Protocol (MCP) tooling integrations.

---

## 🛠️ Development Setup

1. **Fork and Clone the Repository:**
   ```bash
   git clone https://github.com/vkelectronics613-web/vibe-coding-cli.git
   cd vibe-coding-cli
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Export keys for the providers you want to test:
   ```bash
   export ANTHROPIC_API_KEY="your-anthropic-key"
   export GEMINI_API_KEY="your-gemini-key"
   export OPENROUTER_API_KEY="your-openrouter-key"
   ```

---

## 🚀 Adding New Providers & Tools

- **Providers:** Implement provider adapters inheriting the standard provider interface in `ai_<provider>.py` and register them in `router.py`.
- **Tools / MCP:** Ensure any external tool integration exposes clean, type-safe arguments and respects safety checks before touching the host filesystem.

---

## 🧪 Pull Request Guidelines

1. Create a descriptive branch: `git checkout -b feat/add-claude-provider`
2. Follow standard Python PEP-8 conventions.
3. Test interactive CLI execution: `python main.py`
4. Submit a Pull Request with a clear description of the problem solved.
