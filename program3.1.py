import sys
import timeit


def memory_comparison():
    sizes = [1_000, 10_000, 100_000, 1_000_000]

    print("=" * 65)
    print(f"{'N':>12} | {'list (байт)':>14} | {'gen (байт)':>12} | {'Ratio':>8}")
    print("-" * 65)

    for n in sizes:
        data_list = [x ** 2 for x in range(n)]
        data_gen = (x ** 2 for x in range(n))

        list_size = sys.getsizeof(data_list)
        gen_size = sys.getsizeof(data_gen)

        print(f"{n:>12,} | {list_size:>14,} | {gen_size:>12,} | {list_size / gen_size:>7.0f}×")

    print("=" * 65)


def performance_comparison():
    n = 500_000
    repetitions = 5

    time_list = timeit.timeit(
        lambda: sum([x ** 2 for x in range(n)]),
        number=repetitions,
    ) / repetitions

    time_gen = timeit.timeit(
        lambda: sum(x ** 2 for x in range(n)),
        number=repetitions,
    ) / repetitions

    print(f"\nsum() для {n:,} елементів (середнє з {repetitions} запусків):")
    print(f"  list comprehension: {time_list:.4f} с")
    print(f"  generator expression: {time_gen:.4f} с")

    faster = "list" if time_list < time_gen else "generator"
    print(f"  Швидше: {faster}")


def practical_usage():
    words = [
        "Python", "ітератор", "генератор", "yield", "comprehension",
        "дані", "пам'ять", "ефективність", "конвеєр", "ліниві",
        "обчислення", "протокол", "об'єкт", "клас", "функція",
    ]

    longest = max((word for word in words), key=len)
    print(f"Найдовше слово: '{longest}' ({len(longest)} символів)")

    all_nonempty = all(word != "" for word in words)
    print(f"Всі слова непорожні: {all_nonempty}")

    has_long = any(len(word) > 15 for word in words)
    print(f"Є слово > 15 символів: {has_long}")

    csv_line = ",".join(word for word in words)
    print(f"CSV: {csv_line}")

    total_length = sum(len(word) for word in words)
    print(f"Сума довжин: {total_length}")

    word_lengths = {word: len(word) for word in words}
    print(f"Довжини: {word_lengths}")

    numbers = range(1, 101)
    even_squares_sum = sum(number ** 2 for number in numbers if number % 2 == 0)
    print(f"\nСума квадратів парних від 1 до 100: {even_squares_sum}")


def main():
    print(">>> Порівняння використання пам'яті <<<\n")
    memory_comparison()

    print("\n>>> Порівняння продуктивності <<<")
    performance_comparison()

    print("\n>>> Практичне використання generator expression <<<\n")
    practical_usage()


if __name__ == "__main__":
    main()
