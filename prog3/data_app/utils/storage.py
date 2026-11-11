"""Зчитування чисел із текстових файлів у кодуванні UTF-8.

Відсутність файлу перетворюється на власне виключення програми.
"""

from ..core.errors import MissingFileError
from ..core.operations import parse_number, parse_many


def read_number(filename: str) -> float:
    """Зчитує одне число з текстового файлу.

    Args:
        filename (str): Шлях до файлу з одним числом.

    Returns:
        float: Число з файлу.

    Raises:
        MissingFileError: Файл не знайдено.
        InvalidNumberError: У файлі неправильне число.
        OSError: Інша помилка читання файлу.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return parse_number(file.read().strip())
    except FileNotFoundError as error:
        raise MissingFileError(filename) from error


def read_numbers(filename: str) -> list[float]:
    """Зчитує список чисел, по одному на рядок.

    Args:
        filename (str): Шлях до текстового файлу.

    Returns:
        list[float]: Список перевірених чисел.

    Raises:
        MissingFileError: Файл не знайдено.
        InvalidNumberError: У файлі є неправильне число.
        OSError: Інша помилка читання файлу.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return parse_many([line.strip() for line in file if line.strip()])
    except FileNotFoundError as error:
        raise MissingFileError(filename) from error
