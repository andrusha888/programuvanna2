"""Власні виключення для роботи з числами та файлами.

Усі доменні помилки походять від DataError.
"""


class DataError(Exception):
    """Позначає загальну помилку програми.

    Args:
        message (str): Текст помилки, якщо він переданий.

    Returns:
        None: Клас використовується як тип виключення.

    Raises:
        Немає.
    """


class InvalidNumberError(DataError):
    """Повідомляє про неправильне числове значення.

    Args:
        field (str): Назва поля з помилкою.
        value (object): Значення, яке не пройшло перевірку.

    Returns:
        None: Клас створює об'єкт виключення.

    Raises:
        Немає.
    """

    def __init__(self, field: str, value: object) -> None:
        """Зберігає дані про некоректне значення.

        Args:
            field (str): Назва поля.
            value (object): Некоректне значення.

        Returns:
            None: Нічого не повертає.

        Raises:
            Немає.
        """
        self.field = field
        self.value = value
        super().__init__(field, value)

    def __str__(self) -> str:
        """Повертає повідомлення про помилку.

        Args:
            Немає.

        Returns:
            str: Опис некоректного поля та значення.

        Raises:
            Немає.
        """
        return f"Неправильне значення поля '{self.field}': {self.value!r}"


class MissingFileError(DataError):
    """Повідомляє про відсутній файл.

    Args:
        filename (str): Шлях до файлу.

    Returns:
        None: Клас створює об'єкт виключення.

    Raises:
        Немає.
    """

    def __init__(self, filename: str) -> None:
        """Зберігає назву відсутнього файлу.

        Args:
            filename (str): Шлях до файлу.

        Returns:
            None: Нічого не повертає.

        Raises:
            Немає.
        """
        self.filename = filename
        super().__init__(filename)

    def __str__(self) -> str:
        """Формує текст помилки пошуку файлу.

        Args:
            Немає.

        Returns:
            str: Повідомлення з назвою файлу.

        Raises:
            Немає.
        """
        return f"Не вдалося знайти файл: {self.filename}"


class DivisionError(DataError):
    """Повідомляє про неприпустимий дільник.

    Args:
        divisor (float): Значення дільника.

    Returns:
        None: Клас створює об'єкт виключення.

    Raises:
        Немає.
    """

    def __init__(self, divisor: float) -> None:
        """Зберігає неправильний дільник.

        Args:
            divisor (float): Неприпустиме значення.

        Returns:
            None: Нічого не повертає.

        Raises:
            Немає.
        """
        self.divisor = divisor
        super().__init__(divisor)

    def __str__(self) -> str:
        """Повертає повідомлення про неправильний дільник.

        Args:
            Немає.

        Returns:
            str: Опис помилки ділення.

        Raises:
            Немає.
        """
        return f"Неприпустимий дільник: {self.divisor}"
