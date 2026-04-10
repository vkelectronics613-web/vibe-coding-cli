"""
Autonomous Agent — AutoGPT-style task execution.
Breaks tasks into steps, calls tools, iterates to completion.
"""
import json
import re
from router import route_chat
from config import AGENT_PROMPT, MAX_AGENT_ITERATIONS
from tools.file_ops import read_file, write_file, list_files, search_files, file_tree
from tools.code_runner import run_python


# Tool registry
TOOLS = {
    "read_file":    read_file,
    "write_file":   write_file,
    "list_files":   list_files,
    "search_files": search_files,
    "file_tree":    file_tree,
    "run_python":   run_python,
}


def run_agent(task: str) -> str:
    """Execute a task autonomously using the agent loop."""
    print(f"\n  🤖 Agent activated")
    print(f"  📋 Task: {task}")
    print(f"  ⚙  Max iterations: {MAX_AGENT_ITERATIONS}")
    print(f"  {'─' * 44}")

    messages = [
        {"role": "system", "content": AGENT_PROMPT},
        {"role": "user", "content": f"Task: {task}"},
    ]

    for iteration in range(1, MAX_AGENT_ITERATIONS + 1):
        print(f"\n  ▸ Step {iteration}/{MAX_AGENT_ITERATIONS}")

        response = route_chat(messages, stream=True)
        messages.append({"role": "assistant", "content": response})

        # Check for task completion
        if "TASK_COMPLETE" in response:
            print(f"\n  ✅ Task completed in {iteration} step(s)")
            return response

        # Check for tool calls
        tool_call = _extract_tool_call(response)
        if tool_call:
            tool_name = tool_call.get("tool", "")
            tool_args = tool_call.get("args", {})
            print(f"  🔧 Calling: {tool_name}({_format_args(tool_args)})")

            result = _execute_tool(tool_name, tool_args)
            result_preview = result[:200] + "..." if len(result) > 200 else result
            print(f"  📎 Result: {result_preview}")

            messages.append({
                "role": "user",
                "content": f"Tool result for {tool_name}:\n{result}"
            })
        else:
            # No tool call and no completion — ask agent to continue
            messages.append({
                "role": "user",
                "content": "Continue with the next step. Use a tool or say TASK_COMPLETE if done."
            })

    print(f"\n  ⚠ Reached maximum iterations ({MAX_AGENT_ITERATIONS})")
    return response


def _extract_tool_call(text: str) -> dict | None:
    """Extract TOOL_CALL JSON from agent response."""
    match = re.search(r'TOOL_CALL:\s*({.*?})', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    return None


def _execute_tool(name: str, args: dict) -> str:
    """Execute a registered tool safely."""
    if name not in TOOLS:
        return f"Error: Unknown tool '{name}'. Available: {', '.join(TOOLS.keys())}"
    try:
        result = TOOLS[name](**args)
        return str(result) if result is not None else "(no output)"
    except Exception as e:
        return f"Error executing {name}: {e}"


def _format_args(args: dict) -> str:
    """Format args for display."""
    parts = []
    for k, v in args.items():
        val = repr(v)
        if len(val) > 40:
            val = val[:37] + "..."
        parts.append(f"{k}={val}")
    return ", ".join(parts)
