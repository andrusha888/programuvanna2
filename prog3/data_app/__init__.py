"""Пакет для перевірки чисел, обчислень та обробки помилок.

Пакет об'єднує основні операції та власні виключення.
"""

from .core.errors import DataError, InvalidNumberError, MissingFileError, DivisionError
from .core.operations import parse_number, divide_numbers, summarize

__all__ = [
    "DataError",
    "InvalidNumberError",
    "MissingFileError",
    "DivisionError",
    "parse_number",
    "divide_numbers",
]
