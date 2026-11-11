
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import hashlib
import time


def io_bound_task(url: str) -> dict:
    time.sleep(0.5)
    return {"url": url, "status": 200, "size": len(url) * 42}


def cpu_bound_task(n: int) -> dict:
    hasher = hashlib.sha256()
    for i in range(n):
        hasher.update(str(i).encode())
    return {"n": n, "hash": hasher.hexdigest()[:16]}


def risky_task(value: int) -> float:
    if value == 0:
        raise ZeroDivisionError("Ділення на нуль!")
    if value < 0:
        raise ValueError(f"Від'ємне значення: {value}")
    return 1000.0 / value


def benchmark_io_bound():
    urls = [f"https://api.example.com/data/{i}" for i in range(20)]

    start = time.perf_counter()
    sequential = [io_bound_task(url) for url in urls]
    seq_time = time.perf_counter() - start

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        parallel = list(executor.map(io_bound_task, urls))
    par_time = time.perf_counter() - start

    print(f"Завдань: {len(parallel)}")
    print(f"Результати збігаються: {sequential == parallel}")
    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"Потоки (5): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")


def benchmark_cpu_bound():
    tasks = [500_000] * 8

    start = time.perf_counter()
    sequential = [cpu_bound_task(n) for n in tasks]
    seq_time = time.perf_counter() - start

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        parallel = list(executor.map(cpu_bound_task, tasks))
    par_time = time.perf_counter() - start

    print(f"Завдань: {len(parallel)}")
    print(f"Результати збігаються: {sequential == parallel}")
    print(f"Послідовно: {seq_time:.3f} сек")
    print(f"Процеси (4): {par_time:.3f} сек")
    print(f"Прискорення: {seq_time / par_time:.2f}x")


def handle_exceptions():
    values = [10, 5, 0, -3, 8, 2]
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(risky_task, value): value for value in values}
        for future in as_completed(futures):
            value = futures[future]
            try:
                print(f"{value}: {future.result():.2f}")
            except (ZeroDivisionError, ValueError) as error:
                print(f"{value}: {type(error).__name__}: {error}")


def main():
    print("=== I/O-bound: ThreadPoolExecutor ===")
    benchmark_io_bound()
    print("\n=== CPU-bound: ProcessPoolExecutor ===")
    benchmark_cpu_bound()
    print("\n=== Обробка виключень ===")
    handle_exceptions()


if __name__ == "__main__":
    main()
