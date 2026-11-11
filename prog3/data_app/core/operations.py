"""Перетворення чисел, ділення та обчислення підсумків.

Функції перевіряють вхідні дані та піднімають доменні виключення.
"""

from math import isfinite
from .errors import InvalidNumberError, DivisionError


def parse_number(text: str) -> float:
    """Перетворює текст на невід'ємне скінченне число.

    Args:
        text (str): Рядок із числом.

    Returns:
        float: Перевірене числове значення.

    Raises:
        InvalidNumberError: Текст не є числом або число неприпустиме.
    """
    try:
        number = float(text)
    except ValueError as error:
        raise InvalidNumberError("число", text) from error

    if not isfinite(number) or number < 0:
        raise InvalidNumberError("число", text)
    return number


def divide_numbers(first: float, second: float) -> float:
    """Ділить перше число на друге.

    Args:
        first (float): Ділене.
        second (float): Дільник.

    Returns:
        float: Результат ділення.

    Raises:
        DivisionError: Дільник дорівнює нулю.
    """
    if second == 0:
        raise DivisionError(second)
    return first / second


def parse_many(values: list[str]) -> list[float]:
    """Перетворює список рядків на список чисел.

    Args:
        values (list[str]): Рядки з числовими значеннями.

    Returns:
        list[float]: Список перевірених чисел.

    Raises:
        InvalidNumberError: Один із рядків містить неправильне число.
    """
    return [parse_number(value) for value in values]


def summarize(values: list[float]) -> dict[str, float]:
    """Обчислює суму та середнє значення чисел.

    Args:
        values (list[float]): Непорожній список чисел.

    Returns:
        dict[str, float]: Словник із сумою та середнім значенням.

    Raises:
        InvalidNumberError: Список порожній.
    """
    if not values:
        raise InvalidNumberError("список чисел", values)
    return {"сума": sum(values), "середнє": sum(values) / len(values)}
