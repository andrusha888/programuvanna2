"""Точка входу для запуску пакету командою python -m data_app."""

import data_app.utils.storage as storage
from data_app.core import DataError, divide_numbers, parse_number, summarize
from .utils.display import show_result, show_error


def main() -> None:
    """Демонструє читання, обчислення та обробку помилок.

    Args:
        Немає.

    Returns:
        None: Виводить результати в консоль.

    Raises:
        OSError: Можлива інша помилка доступу до файлу.
    """
    print("Успішне виконання:")
    try:
        number = storage.read_number("sample_data.txt")
        show_result("Прочитано число", number)
        show_result("Результат ділення на 3", divide_numbers(number, 3.0))
        print("Підсумок:", summarize([number, 30.0]))
    except DataError as error:
        show_error(error)

    print("\nОбробка помилок:")
    for action in (
        lambda: storage.read_number("відсутній_файл_12345.txt"),
        lambda: parse_number("не число"),
        lambda: divide_numbers(10.0, 0.0),
    ):
        try:
            action()
        except DataError as error:
            show_error(error)
            if error.__cause__ is not None:
                print("Причина:", type(error.__cause__).__name__)


if __name__ == "__main__":
    main()
