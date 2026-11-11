import multiprocessing
import os
import time


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def sum_primes_in_range(start: int, end: int) -> tuple[int, int, int]:
    total = 0
    count = 0
    for number in range(start, end):
        if is_prime(number):
            total += number
            count += 1
    return total, count, os.getpid()


def main():
    total_range = 1_000_000
    num_workers = 4
    chunk_size = total_range // num_workers
    ranges = []

    for i in range(num_workers):
        start = max(2, i * chunk_size)
        end = total_range if i == num_workers - 1 else (i + 1) * chunk_size
        ranges.append((start, end))

    start_time = time.perf_counter()
    sequential_results = [sum_primes_in_range(a, b) for a, b in ranges]
    seq_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    with multiprocessing.Pool(processes=num_workers) as pool:
        parallel_results = pool.starmap(sum_primes_in_range, ranges)
    par_time = time.perf_counter() - start_time

    total_sum = sum(result[0] for result in parallel_results)
    prime_count = sum(result[1] for result in parallel_results)

    print(f"Сума простих чисел: {total_sum}")
    print(f"Кількість простих чисел: {prime_count}")
    print("Робочі процеси:")
    for (begin, end), result in zip(ranges, parallel_results):
        print(f"  [{begin}, {end}): PID {result[2]}, простих: {result[1]}")

    print(f"Результати збігаються: {[(x[0], x[1]) for x in sequential_results] == [(x[0], x[1]) for x in parallel_results]}")
    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"Паралельно ({num_workers} процеси): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
