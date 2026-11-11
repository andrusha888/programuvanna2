"""Порівняння структури Django- та Flask-проєктів."""

import os


IGNORED_DIRS = {"venv", "venv2", ".venv", "__pycache__", ".git", ".idea", ".pytest_cache"}
IGNORED_FILES = {"db.sqlite3", ".env"}


def valid_name(name: str, is_dir: bool) -> bool:
    if is_dir:
        return name not in IGNORED_DIRS
    return name not in IGNORED_FILES and not name.endswith(".pyc")


def scan_directory(path: str, prefix: str = "") -> list[str]:
    tree = []
    entries = sorted(
        [entry for entry in os.scandir(path) if valid_name(entry.name, entry.is_dir())],
        key=lambda entry: (not entry.is_dir(), entry.name.lower()),
    )
    for index, entry in enumerate(entries):
        last = index == len(entries) - 1
        branch = "└── " if last else "├── "
        tree.append(prefix + branch + entry.name + ("/" if entry.is_dir() else ""))
        if entry.is_dir():
            indent = "    " if last else "│   "
            tree.extend(scan_directory(entry.path, prefix + indent))
    return tree


def analyze_project(path: str) -> dict:
    stats = {
        "py_files": 0,
        "html_files": 0,
        "css_files": 0,
        "total_size": 0,
        "directories": [],
    }
    for folder, dirs, files in os.walk(path):
        dirs[:] = sorted(name for name in dirs if valid_name(name, True))
        if folder != path:
            stats["directories"].append(os.path.relpath(folder, path))
        for name in files:
            if not valid_name(name, False):
                continue
            file_path = os.path.join(folder, name)
            stats["total_size"] += os.path.getsize(file_path)
            if name.endswith(".py"):
                stats["py_files"] += 1
            elif name.endswith(".html"):
                stats["html_files"] += 1
            elif name.endswith(".css"):
                stats["css_files"] += 1
    return stats


def compare_projects(django_path: str, flask_path: str):
    print("=== ПОРІВНЯННЯ СТРУКТУРИ ПРОЄКТІВ ===")
    for title, path in (("Django", django_path), ("Flask", flask_path)):
        print(f"\n--- {title} ({path}) ---")
        for line in scan_directory(path):
            print(line)

    django = analyze_project(django_path)
    flask = analyze_project(flask_path)
    items = [
        ("Файли .py", "py_files"),
        ("Файли .html", "html_files"),
        ("Файли .css", "css_files"),
        ("Каталоги", "directories"),
        ("Розмір (байт)", "total_size"),
    ]
    print(f"\n{'Характеристика':<22}{'Django':>12}{'Flask':>12}")
    print("-" * 46)
    for title, key in items:
        d = len(django[key]) if key == "directories" else django[key]
        f = len(flask[key]) if key == "directories" else flask[key]
        print(f"{title:<22}{d:>12}{f:>12}")


def main():
    django_path = "mysite"
    flask_path = "myflaskapp"
    for path in (django_path, flask_path):
        if not os.path.isdir(path):
            print(f"Каталог '{path}' не знайдено. Запустіть скрипт із кореня практичної.")
            return
    compare_projects(django_path, flask_path)


if __name__ == "__main__":
    main()
