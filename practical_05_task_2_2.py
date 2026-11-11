"""Перегляд основних налаштувань Django та перевірка безпеки."""

import ast
import os
import sys


def read_assignments(settings_path: str) -> dict:
    with open(settings_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())
    assignments = {}
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    assignments[target.id] = statement.value
    return assignments


def get_literal(assignments: dict, name: str, default=None):
    try:
        return ast.literal_eval(assignments[name])
    except (KeyError, ValueError, TypeError, SyntaxError):
        return default


def analyze_settings(settings_path: str) -> dict:
    assignments = read_assignments(settings_path)
    engines = []
    database = assignments.get("DATABASES")
    if database:
        engines = [node.value for node in ast.walk(database)
                   if isinstance(node, ast.Constant)
                   and isinstance(node.value, str)
                   and node.value.startswith("django.db.backends.")]
    return {
        "DEBUG": os.environ.get("DJANGO_DEBUG", "1") == "1",
        "INSTALLED_APPS": get_literal(assignments, "INSTALLED_APPS", []),
        "DATABASES": engines[0] if engines else "не визначено",
        "LANGUAGE_CODE": get_literal(assignments, "LANGUAGE_CODE", "не визначено"),
        "TIME_ZONE": get_literal(assignments, "TIME_ZONE", "не визначено"),
    }


def check_security(settings_path: str) -> list[str]:
    assignments = read_assignments(settings_path)
    warnings = []
    if analyze_settings(settings_path)["DEBUG"]:
        warnings.append("DEBUG увімкнено: підходить для розробки, але не для production")

    secret = assignments.get("SECRET_KEY")
    if secret is None:
        warnings.append("SECRET_KEY не знайдено")
    elif "os.environ" not in ast.unparse(secret):
        warnings.append("SECRET_KEY не зчитується із змінної оточення")

    hosts = get_literal(assignments, "ALLOWED_HOSTS", [])
    if not hosts:
        warnings.append("ALLOWED_HOSTS порожній")
    return warnings


def main():
    settings_path = os.path.join("mysite", "mysite", "settings.py")
    if not os.path.exists(settings_path):
        print(f"Файл {settings_path} не знайдено. Запустіть скрипт із кореня практичної.")
        sys.exit(1)

    print("=== Аналіз конфігурації Django ===")
    for key, value in analyze_settings(settings_path).items():
        print(f"{key}: {value}")

    print("\n=== Перевірка безпеки ===")
    warnings = check_security(settings_path)
    if warnings:
        for warning in warnings:
            print(f"Попередження: {warning}")
    else:
        print("Попереджень не знайдено")


if __name__ == "__main__":
    main()
