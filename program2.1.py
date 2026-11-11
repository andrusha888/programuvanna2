import functools
import time


def cache(max_size: int = 128):
    if max_size < 1:
        raise ValueError("Розмір кешу має бути додатним")

    def decorator(func):
        saved = {}
        order = []

        @functools.wraps(func)
        def wrapper(*args):
            if args in saved:
                order.remove(args)
                order.append(args)
                print(f"cache hit: {func.__name__}{args}")
                return saved[args]

            print(f"cache miss: {func.__name__}{args}")
            result = func(*args)
            saved[args] = result
            order.append(args)
            if len(order) > max_size:
                oldest = order.pop(0)
                del saved[oldest]
            return result

        wrapper.cache_info = lambda: {"size": len(saved), "max_size": max_size}

        def clear():
            saved.clear()
            order.clear()

        wrapper.cache_clear = clear
        return wrapper

    return decorator


def rate_limit(max_calls: int, period: float = 60.0):
    def decorator(func):
        call_times = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic()
            call_times[:] = [moment for moment in call_times if now - moment < period]
            if len(call_times) >= max_calls:
                raise RuntimeError("Перевищено ліміт викликів")
            call_times.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log(level: str = "INFO"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Виклик {func.__name__}{args}, {kwargs}")
            started = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                print(f"[ERROR] {func.__name__}: {error}")
                raise
            elapsed = time.perf_counter() - started
            print(f"[{level}] {func.__name__} -> {result} (час: {elapsed:.4f}с)")
            return result

        return wrapper

    return decorator


@cache(max_size=64)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@rate_limit(max_calls=5, period=10.0)
def send_notification(message: str) -> str:
    return f"Надіслано: {message}"


@log(level="DEBUG")
def divide(a: float, b: float) -> float:
    return a / b


def main():
    print("Обчислення Фібоначчі:")
    print("fibonacci(30) =", fibonacci(30))
    print("Повторно fibonacci(30) =", fibonacci(30))
    print("Інформація про кеш:", fibonacci.cache_info())

    print("\nЛіміт викликів:")
    for number in range(1, 7):
        try:
            print(send_notification(f"Повідомлення {number}"))
        except RuntimeError as error:
            print("Помилка:", error)

    print("\nЛогування ділення:")
    print("Результат:", divide(10, 3))
    try:
        divide(10, 0)
    except ZeroDivisionError:
        print("Помилку ділення перехоплено")


if __name__ == "__main__":
    main()
