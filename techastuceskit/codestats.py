"""codestats.py — quick stats about a codebase: lines per language, TODOs."""

import os
from pathlib import Path
from collections import defaultdict

EXTENSIONS = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".jsx": "React",
    ".tsx": "React/TS", ".html": "HTML", ".css": "CSS", ".php": "PHP",
    ".java": "Java", ".c": "C", ".cpp": "C++", ".go": "Go", ".rb": "Ruby",
    ".json": "JSON", ".md": "Markdown", ".sh": "Shell",
}

IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
TODO_MARKERS = ("TODO", "FIXME", "XXX", "HACK")


def run(path: str):
    root = Path(path).resolve()
    if not root.exists():
        print(f"❌ Directory not found: {root}")
        return

    lines_per_lang = defaultdict(int)
    files_per_lang = defaultdict(int)
    todos = []
    total_lines = 0
    total_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for name in filenames:
            ext = Path(name).suffix
            lang = EXTENSIONS.get(ext)
            if not lang:
                continue

            full_path = Path(dirpath) / name
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    file_lines = f.readlines()
            except (PermissionError, OSError):
                continue

            n = len(file_lines)
            lines_per_lang[lang] += n
            files_per_lang[lang] += 1
            total_lines += n
            total_files += 1

            for i, line in enumerate(file_lines, 1):
                if any(marker in line for marker in TODO_MARKERS):
                    rel = full_path.relative_to(root)
                    todos.append(f"{rel}:{i}  {line.strip()[:70]}")

    print(f"📊 Code Stats — {root}\n")
    print(f"{total_files} files, {total_lines:,} lines total\n")

    print(f"{'Language':15} {'Files':10} {'Lines':10}")
    print("-" * 37)
    for lang, lines in sorted(lines_per_lang.items(), key=lambda x: -x[1]):
        print(f"{lang:15} {files_per_lang[lang]:<10} {lines:,}")

    if todos:
        print(f"\n📌 {len(todos)} TODO/FIXME found:")
        for t in todos[:20]:
            print(f"  {t}")
        if len(todos) > 20:
            print(f"  ... and {len(todos) - 20} more")
    else:
        print("\n✅ No pending TODO/FIXME.")
