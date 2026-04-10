"""
File system operations for the AI agent.
All operations are scoped to the current working directory for safety.
"""
import os
import fnmatch


def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file (creates directories if needed)."""
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✓ Written: {path} ({len(content)} bytes)"
    except Exception as e:
        return f"Error writing file: {e}"


def list_files(directory: str = ".") -> str:
    """List all files and directories in the given path."""
    try:
        entries = sorted(os.listdir(directory))
        if not entries:
            return "(empty directory)"
        lines = []
        for entry in entries:
            full = os.path.join(directory, entry)
            prefix = "📁" if os.path.isdir(full) else "📄"
            lines.append(f"  {prefix} {entry}")
        return "\n".join(lines)
    except FileNotFoundError:
        return f"Error: Directory not found: {directory}"
    except Exception as e:
        return f"Error listing directory: {e}"


def search_files(directory: str = ".", pattern: str = "*") -> str:
    """Search for files matching a glob pattern."""
    try:
        matches = []
        for root, dirs, files in os.walk(directory):
            # Skip hidden and common junk directories
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "__pycache__", ".git")]
            for fname in files:
                if fnmatch.fnmatch(fname, pattern):
                    matches.append(os.path.join(root, fname))
        if not matches:
            return f"No files matching '{pattern}' found in {directory}"
        return "\n".join(f"  📄 {m}" for m in matches[:50])
    except Exception as e:
        return f"Error searching: {e}"


def file_tree(directory: str = ".", max_depth: int = 3) -> str:
    """Display a visual directory tree."""
    try:
        lines = [f"  {directory}/"]
        _tree_walk(directory, "", max_depth, 0, lines)
        return "\n".join(lines)
    except Exception as e:
        return f"Error building tree: {e}"


def _tree_walk(path: str, prefix: str, max_depth: int, depth: int, lines: list):
    """Recursive helper for file_tree."""
    if depth >= max_depth:
        return
    try:
        entries = sorted(os.listdir(path))
        entries = [e for e in entries if not e.startswith(".") and e not in ("node_modules", "__pycache__")]
    except PermissionError:
        return

    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        full = os.path.join(path, entry)
        icon = "📁" if os.path.isdir(full) else "📄"
        lines.append(f"  {prefix}{connector}{icon} {entry}")
        if os.path.isdir(full):
            extension = "    " if is_last else "│   "
            _tree_walk(full, prefix + extension, max_depth, depth + 1, lines)
