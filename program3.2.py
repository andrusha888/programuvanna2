def calculator():
    print("=== Калькулятор ===")
    print("Введіть вираз у форматі: число оператор число")
    print("Введіть 'quit' для виходу, 'history' для історії")

    history = []

    while True:
        user_input = input("\n> ").strip()

        if user_input.lower() == "quit":
            print("Роботу калькулятора завершено")
            break

        if user_input.lower() == "history":
            if history:
                for record in history:
                    print(record)
            else:
                print("Історія поки порожня")
            continue

        parts = user_input.split()
        if len(parts) != 3:
            print("Помилка: введіть число оператор число")
            continue

        first, operator, second = parts
        try:
            a = float(first)
            b = float(second)
        except ValueError:
            print("Помилка: потрібно вводити числа")
            continue

        if operator not in ("+", "-", "*", "/", "//", "%", "**"):
            print("Помилка: невідомий оператор")
            continue

        try:
            if operator == "+":
                result = a + b
            elif operator == "-":
                result = a - b
            elif operator == "*":
                result = a * b
            elif operator == "/":
                result = a / b
            elif operator == "//":
                result = a // b
            elif operator == "%":
                result = a % b
            else:
                result = a ** b
        except ZeroDivisionError:
            print("Помилка: ділення на нуль")
            continue
        except OverflowError:
            print("Помилка: завелике число")
            continue

        record = f"{a:g} {operator} {b:g} = {result}"
        history.append(record)
        print(record)


if __name__ == "__main__":
    calculator()
