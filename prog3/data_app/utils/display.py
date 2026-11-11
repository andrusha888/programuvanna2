"""Допоміжні функції для зрозумілого виведення в консоль."""

from ..core.errors import DataError


def show_result(label: str, value: float) -> None:
    """Виводить назву та числовий результат.

    Args:
        label (str): Підпис результату.
        value (float): Число для виведення.

    Returns:
        None: Виводить текст у консоль.

    Raises:
        Немає.
    """
    print(f"{label}: {value:.2f}")


def show_error(error: DataError) -> None:
    """Виводить пояснення помилки програми.

    Args:
        error (DataError): Перехоплене доменне виключення.

    Returns:
        None: Виводить текст у консоль.

    Raises:
        Немає.
    """
    print("Помилка:", error)
