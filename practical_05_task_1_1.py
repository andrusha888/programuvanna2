"""Перевірка версії Python та встановлених фреймворків."""

import sys
from importlib import import_module, metadata


def check_python_version():
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version < (3, 10):
        print("Попередження: потрібен Python 3.10 або новіший")
        return False
    print("Версія Python підходить")
    return True


def check_package(package_name: str) -> bool:
    try:
        import_module(package_name)
        version = metadata.version(package_name)
        print(f"  {package_name}: {version} - встановлено")
        return True
    except (ImportError, metadata.PackageNotFoundError):
        print(f"  {package_name}: не встановлено")
        return False


def main():
    check_python_version()
    print("\nВстановлені пакети:")
    packages = ["django", "flask"]
    results = {name: check_package(name) for name in packages}
    installed = sum(results.values())
    missing = [name for name, is_installed in results.items() if not is_installed]
    print(f"\nВстановлено: {installed}, відсутні: {len(missing)}")
    if missing:
        print("Для встановлення виконайте:")
        print(f"python -m pip install {' '.join(missing)}")


if __name__ == "__main__":
    main()
