"""Основна логіка програми та її власні виключення."""

from .errors import DataError, InvalidNumberError, MissingFileError, DivisionError
from .operations import parse_number, divide_numbers, parse_many, summarize

__all__ = [
    "DataError",
    "InvalidNumberError",
    "MissingFileError",
    "DivisionError",
    "parse_number",
    "divide_numbers",
    "parse_many",
    "summarize",
]
