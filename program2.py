class DataError(Exception):
    pass


class InvalidNumberError(DataError):
    def __init__(self, field, value):
        self.field = field
        self.value = value
        super().__init__(field, value)

    def __str__(self):
        return f"Неправильне значення поля '{self.field}': {self.value!r}"


class MissingFileError(DataError):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(filename)

    def __str__(self):
        return f"Не вдалося знайти файл: {self.filename}"


class DivisionError(DataError):
    def __init__(self, divisor):
        self.divisor = divisor
        super().__init__(divisor)

    def __str__(self):
        return f"Неприпустимий дільник: {self.divisor}"


def read_number(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read().strip()
    except FileNotFoundError as error:
        raise MissingFileError(filename) from error

    try:
        number = float(content)
    except ValueError as error:
        raise InvalidNumberError("число", content) from error

    if number < 0:
        raise InvalidNumberError("число", number)
    return number


def divide_numbers(first, second):
    if second == 0:
        raise DivisionError(second)
    return first / second


def logged_division(first, second):
    try:
        return divide_numbers(first, second)
    except DivisionError as error:
        print("Запис у журнал:", error)
        raise


if __name__ == "__main__":
    with open("число_для_перевірки.txt", "w", encoding="utf-8") as file:
        file.write("120")

    with open("помилкове_число.txt", "w", encoding="utf-8") as file:
        file.write("текст")

    print("Успішне читання:", read_number("число_для_перевірки.txt"))

    try:
        read_number("помилкове_число.txt")
    except InvalidNumberError as error:
        print("Конкретна помилка:", error)

    try:
        read_number("відсутній_файл_12345.txt")
    except MissingFileError as error:
        print("Конкретна помилка:", error)
        print("Початкова причина:", type(error.__cause__).__name__)

    try:
        logged_division(10, 0)
    except DataError as error:
        print("Перехоплено через базовий DataError:", error)

    print("Успішне ділення:", logged_division(10, 2))
