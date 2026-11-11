def factorial(n: int) -> int:
    result = 1
    for number in range(2, n + 1):
        result *= number
    return result


def harmonic_sum(n: int) -> float:
    total = 0
    for number in range(1, n + 1, 1):
        total += 1 / number
    return total


def multiplication_table(n: int) -> None:
    print(" " * 5 + "".join(f"{number:>5}" for number in range(1, n + 1)))
    for row in range(1, n + 1):
        print(f"{row:>4} " + "".join(f"{row * column:>5}" for column in range(1, n + 1)))


def main():
    try:
        n = int(input("Введіть число n: "))
    except ValueError:
        print("Помилка: потрібно ввести ціле число")
        return

    if n <= 0:
        print("Помилка: n має бути додатним")
        return

    print(f"{n}! = {factorial(n)}")
    print(f"Гармонічна сума H({n}) = {harmonic_sum(n):.6f}")
    print(f"\nТаблиця множення {n}×{n}:")
    multiplication_table(n)


if __name__ == "__main__":
    main()
