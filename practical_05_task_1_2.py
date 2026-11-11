"""Отримання, збереження та перевірка версій пакетів."""

import json
import re
import subprocess
import sys


def get_installed_packages() -> list[dict]:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=json"],
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def normalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def generate_requirements(packages: list[dict], filename: str = "requirements.txt"):
    excluded = {"pip", "setuptools", "wheel"}
    selected = [
        package for package in packages
        if normalize_name(package["name"]) not in excluded
    ]
    selected.sort(key=lambda package: normalize_name(package["name"]))
    with open(filename, "w", encoding="utf-8") as file:
        for package in selected:
            file.write(f'{package["name"]}=={package["version"]}\n')


def verify_requirements(filename: str = "requirements.txt") -> bool:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Помилка: файл {filename} не знайдено")
        return False

    installed = {
        normalize_name(item["name"]): item["version"]
        for item in get_installed_packages()
    }
    all_correct = True
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            print(f"Невідомий формат залежності: {line}")
            all_correct = False
            continue
        name, expected_version = line.split("==", 1)
        actual = installed.get(normalize_name(name))
        if actual != expected_version:
            print(f"Розбіжність для {name}: очікується {expected_version}, встановлено {actual}")
            all_correct = False
    return all_correct


def main():
    try:
        packages = get_installed_packages()
    except (subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"Не вдалося отримати список пакетів: {error}")
        return
    print(f"Знайдено {len(packages)} встановлених пакетів")
    for package in packages[:10]:
        print(f'  {package["name"]}=={package["version"]}')
    generate_requirements(packages)
    print("Файл requirements.txt створено")
    print("Перевірка залежностей:", "усе правильно" if verify_requirements() else "є розбіжності")


if __name__ == "__main__":
    main()
