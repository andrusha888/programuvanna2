def main():
    raw_input = input("Введіть число: ")

    try:
        float_value = float(raw_input)
        int_value = int(float_value)
    except (ValueError, OverflowError):
        print("Помилка: введене значення не є звичайним числом")
        return

    bool_value = bool(float_value)
    string_value = str(int_value)

    print(f"Рядок: {raw_input}, тип: {type(raw_input).__name__}")
    print(f"Ціле число: {int_value}, тип: {type(int_value).__name__}")
    print(f"Дійсне число: {float_value:.2f}, тип: {type(float_value).__name__}")
    print(f"Логічне значення: {bool_value}, тип: {type(bool_value).__name__}")
    print(f"Перетворення в рядок: {string_value}, тип: {type(string_value).__name__}")
    print(f"Перевірка isinstance: {isinstance(float_value, float)}")

    name = input("Введіть ім'я: ").strip()
    try:
        age = int(input("Введіть вік: "))
    except ValueError:
        print("Помилка: вік потрібно вводити цілим числом")
        return

    print(f"Ім'я з вирівнюванням: {name:<15} | Вік: {age:03d}")
    print(f"Число з двома знаками: {float_value:.2f}")
    print(f"Ціле число з нулями: {int_value:06d}")

    numbers = list(range(1, 6))
    print(f"Список з range(): {numbers}")
    print(f"Довжина списку: {len(numbers)}")
    print(f"Довжина імені: {len(name)}")
    print(f"Ідентифікатор списку: {id(numbers)}")


if __name__ == "__main__":
    main()
