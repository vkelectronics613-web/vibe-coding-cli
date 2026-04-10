#!/usr/bin/env python3
import sys
import os
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.live import Live
from rich import box

from config import IMAGE_API_KEY, IMAGE_API_URL, GEMINI_API_KEY, OPENROUTER_API_KEY
from memory import Memory
from router import route_stream
from agent import run_agent
from tools.file_ops import read_file, write_file, list_files, search_files, tree
from tools.code_runner import run_file as exec_file

# 🌑 FORCE MODERN TERMINAL COLORS
console = Console(force_terminal=True, color_system="truecolor")
memory = Memory()

# 🎨 GOOGLE THEME COLORS
BLUE = "bright_blue"
RED = "bright_red"
YELLOW = "bright_yellow"
GREEN = "bright_green"
WHITE = "white"
DIM = "grey62"

# ───────────────────────────────────────────────

def print_banner():
    console.print()
    console.print(Panel.fit(
        f"[bold {BLUE}]G[/bold {BLUE}]"
        f"[bold {RED}]e[/bold {RED}]"
        f"[bold {YELLOW}]m[/bold {YELLOW}]"
        f"[bold {BLUE}]i[/bold {BLUE}]"
        f"[bold {GREEN}]n[/bold {GREEN}]"
        f"[bold {RED}]i[/bold {RED}]  "
        f"[bold white]VIRAT PRO[/bold white]\n\n"
        f"[{DIM}]AI Coding Assistant CLI[/]\n"
        f"[{DIM}]Gemini • OpenRouter • Autonomous Agents[/]",
        border_style=BLUE,
        padding=(1, 4)
    ))
    console.print()

# ───────────────────────────────────────────────

def print_status():
    table = Table(box=box.ROUNDED, border_style=BLUE)
    table.add_column("Service", style=f"bold {BLUE}")
    table.add_column("Status")
    table.add_column("Model", style="dim")

    table.add_row(
        "✦ Gemini",
        f"[{GREEN}]● Connected[/{GREEN}]" if GEMINI_API_KEY else f"[{RED}]○ Missing[/{RED}]",
        "gemini-2.0-flash" if GEMINI_API_KEY else "-"
    )
    table.add_row(
        "⚡ OpenRouter",
        f"[{GREEN}]● Connected[/{GREEN}]" if OPENROUTER_API_KEY else f"[{RED}]○ Missing[/{RED}]",
        "mistral / llama"
    )
    table.add_row(
        "🎨 Image",
        f"[{GREEN}]● Ready[/{GREEN}]" if IMAGE_API_KEY else f"[{YELLOW}]○ Optional[/{YELLOW}]",
        "image API"
    )

    console.print(table)
    console.print(f"[{DIM}]Memory: {memory.summary()}[/]")
    console.print(f"[{DIM}]Dir: {os.getcwd()}[/]\n")

# ───────────────────────────────────────────────

def print_help():
    table = Table(box=box.SIMPLE_HEAVY, border_style=BLUE)
    table.add_column("Command", style=f"bold {BLUE}")
    table.add_column("Description")

    cmds = [
        ("/chat", "Ask AI anything"),
        ("/code", "Generate code"),
        ("/fix", "Fix errors"),
        ("/agent", "Autonomous AI"),
        ("/search", "Search files"),
        ("/image", "Generate image"),
        ("/file", "File operations"),
        ("/run", "Run file"),
        ("/memory", "Show memory"),
        ("/clear", "Clear memory"),
        ("/help", "Show help"),
        ("exit", "Quit"),
    ]

    for c, d in cmds:
        table.add_row(c, d)

    console.print(Panel(table, title="⚡ Commands", border_style=BLUE))

# ───────────────────────────────────────────────

def stream_response(messages, task="chat"):
    full = ""

    with Live(console=console, refresh_per_second=15) as live:
        for chunk in route_stream(messages, task):
            full += chunk
            live.update(Panel(
                Markdown(full),
                border_style=BLUE
            ))
            time.sleep(0.01)  # smooth typing

    console.print(Panel(
        Markdown(full),
        title=f"[bold {BLUE}]✦ Response[/]",
        border_style=BLUE
    ))
    return full

# ───────────────────────────────────────────────

def handle_chat(prompt):
    memory.add("user", prompt)
    msgs = [{"role": "system", "content": "You are a helpful AI."}, *memory.get_context()]
    res = stream_response(msgs, "chat")
    memory.add("assistant", res)

def handle_code(prompt):
    memory.add("user", prompt)
    msgs = [{"role": "system", "content": "You are an expert programmer."}, *memory.get_context()]
    res = stream_response(msgs, "code")
    memory.add("assistant", res)

def handle_fix(err):
    memory.add("user", err)
    msgs = [{"role": "system", "content": "Fix errors clearly."}, *memory.get_context()]
    res = stream_response(msgs, "fix")
    memory.add("assistant", res)

# ───────────────────────────────────────────────

def handle_image(prompt):
    if not IMAGE_API_KEY:
        console.print(f"[{RED}]❌ No IMAGE_API_KEY[/]")
        return

    console.print(f"[{DIM}]🎨 Generating...[/]")

    try:
        r = requests.post(IMAGE_API_URL, json={"api_key": IMAGE_API_KEY, "prompt": prompt})
        data = r.json()

        if "imageUrl" in data:
            console.print(Panel(
                f"[bold {GREEN}]✅ Image Generated[/]\n\n{data['imageUrl']}",
                border_style=GREEN
            ))
        else:
            console.print(data)
    except Exception as e:
        console.print(f"[{RED}]Error: {e}[/]")

# ───────────────────────────────────────────────

def get_prompt():
    try:
        console.print(f"\n[bold {BLUE}]●[/] [bold white]gemini[/]", end="")
        return console.input(f"\n[bold {GREEN}]❯[/] ").strip()
    except:
        return "exit"

# ───────────────────────────────────────────────

def main():
    print_banner()
    print_status()
    print_help()

    while True:
        user = get_prompt()

        if user in ("exit", "quit"):
            console.print(f"[{BLUE}]👋 Bye Virat Kumar[/]")
            break

        if user.startswith("/"):
            cmd, *args = user.split(" ", 1)
            arg = args[0] if args else ""

            if cmd == "/chat":
                handle_chat(arg)
            elif cmd == "/code":
                handle_code(arg)
            elif cmd == "/fix":
                handle_fix(arg)
            elif cmd == "/agent":
                run_agent(arg, memory)
            elif cmd == "/image":
                handle_image(arg)
            elif cmd == "/help":
                print_help()
            else:
                console.print(f"[{YELLOW}]Unknown command[/]")

        else:
            handle_chat(user)

# ───────────────────────────────────────────────

if __name__ == "__main__":
    main()
