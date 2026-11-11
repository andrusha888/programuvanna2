import math


def main():
    try:
        a = float(input("Введіть a: "))
        b = float(input("Введіть b: "))
        c = float(input("Введіть c: "))
    except ValueError:
        print("Помилка: потрібно вводити числа")
        return

    sum_squares = a ** 2 + b ** 2 + c ** 2
    average = (a + b + c) / 3
    discriminant = b ** 2 - 4 * a * c
    hypotenuse = math.sqrt(a ** 2 + b ** 2)
    invalid_sides = a <= 0 or b <= 0 or c <= 0
    is_triangle = not invalid_sides and a + b > c and a + c > b and b + c > a

    print(f"Сума квадратів: {sum_squares:.2f}")
    print(f"Середнє арифметичне: {average:.2f}")
    print(f"Дискримінант: {discriminant:.2f}")
    print(f"Гіпотенуза: {hypotenuse:.2f}")
    print(f"Чи утворюють числа трикутник: {'Так' if is_triangle else 'Ні'}")

    if b != 0:
        print(f"Ділення a / b: {a / b:.2f}")
        print(f"Цілочисельне ділення a // b: {a // b:.2f}")
        print(f"Остача від ділення a % b: {a % b:.2f}")
    else:
        print("Ділення на b неможливе, оскільки b дорівнює нулю")


if __name__ == "__main__":
    main()
