def basic_check(value):
    print(f"\n1. Базовий try/except, вхід: {value!r}")
    try:
        number = int(value)
        print("Отримане ціле число:", number)
    except ValueError:
        print("Помилка ValueError: потрібно ввести ціле число")


def file_check(filename):
    print(f"\n2. try/except/else/finally, файл: {filename}")
    try:
        with open(filename, "r", encoding="utf-8") as file:
            number = int(file.read().strip())
    except FileNotFoundError:
        print("Помилка FileNotFoundError: файл не знайдено")
    except ValueError:
        print("Помилка ValueError: вміст файлу не є цілим числом")
    else:
        print("else: успішно прочитано число", number)
    finally:
        print("finally: обробку файлу завершено")


def division_check(first, second):
    print(f"\n3. Один except для двох помилок, дані: {first!r} і {second!r}")
    try:
        result = float(first) / float(second)
        print("Результат ділення:", result)
    except (ValueError, ZeroDivisionError) as error:
        print(f"Помилка {type(error).__name__}: {error}")


if __name__ == "__main__":
    with open("правильне_число.txt", "w", encoding="utf-8") as file:
        file.write("45")

    with open("неправильне_число.txt", "w", encoding="utf-8") as file:
        file.write("сорок п'ять")

    basic_check("25")
    basic_check("двадцять")

    file_check("правильне_число.txt")
    file_check("неправильне_число.txt")
    file_check("немає_такого_файлу_12345.txt")

    division_check("12", "3")
    division_check("abc", "3")
    division_check("12", "0")
