import math


def triangle_type(a: float, b: float, c: float) -> str:
    if a <= 0 or b <= 0 or c <= 0:
        return "не є трикутником"
    else:
        if a + b <= c or a + c <= b or b + c <= a:
            return "не є трикутником"
        else:
            sides = sorted([a, b, c])
            if a == b and b == c:
                return "рівносторонній"
            elif abs(sides[0] ** 2 + sides[1] ** 2 - sides[2] ** 2) < 1e-9:
                return "прямокутний"
            elif a == b or a == c or b == c:
                return "рівнобедрений"
            else:
                return "різносторонній"


def triangle_area(a: float, b: float, c: float) -> float:
    p = (a + b + c) / 2
    return math.sqrt(max(0, p * (p - a) * (p - b) * (p - c)))


def main():
    try:
        a = float(input("Введіть сторону a: "))
        b = float(input("Введіть сторону b: "))
        c = float(input("Введіть сторону c: "))
    except ValueError:
        print("Помилка: потрібно вводити числа")
        return

    kind = triangle_type(a, b, c)
    print(f"Тип трикутника: {kind}")

    if kind != "не є трикутником":
        print(f"Площа трикутника: {triangle_area(a, b, c):.2f}")
    else:
        print("Площу обчислити неможливо")


if __name__ == "__main__":
    main()
