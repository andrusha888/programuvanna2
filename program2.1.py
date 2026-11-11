import itertools


def arithmetic_progression(start: float, step: float):
    current = start
    while True:
        yield current
        current += step


def geometric_progression(start: float, ratio: float, limit: float = float("inf")):
    if start <= 0 or ratio <= 1:
        raise ValueError("Початок має бути додатним, а множник більшим за 1")

    current = start
    while current <= limit and current != float("inf"):
        yield current
        current *= ratio


def fibonacci(n: int | None = None):
    if n is not None and n < 0:
        raise ValueError("Кількість чисел не може бути від'ємною")

    a, b = 0, 1
    count = 0

    while n is None or count < n:
        yield a
        a, b = b, a + b
        count += 1


def collatz_sequence(n: int):
    if n <= 0:
        raise ValueError("Число повинно бути додатним")

    while True:
        yield n
        if n == 1:
            break
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1


def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def main():
    ap = arithmetic_progression(2, 3)
    first_10 = list(itertools.islice(ap, 10))
    print(f"Арифметична прогресія (2, 3): {first_10}")

    gp = list(geometric_progression(1, 2, limit=1000))
    print(f"Геометрична прогресія (1, 2): {gp}")

    fib_15 = list(fibonacci(15))
    print(f"Фібоначчі (15): {fib_15}")

    coll = list(collatz_sequence(27))
    print(f"Коллатц (27): довжина={len(coll)}, макс={max(coll)}")

    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    flat = list(flatten(nested))
    print(f"Розгортання: {flat}")

    for fib_num in fibonacci(None):
        if fib_num > 10000:
            print(f"Перше число Фібоначчі > 10000: {fib_num}")
            break


if __name__ == "__main__":
    main()
