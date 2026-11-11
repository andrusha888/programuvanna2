import random
import threading
import time


class ConnectionPool:
    def __init__(self, max_connections: int = 3):
        self._semaphore = threading.Semaphore(max_connections)
        self._lock = threading.Lock()
        self.max_connections = max_connections
        self.active_connections = 0
        self.total_served = 0
        self.peak_connections = 0

    def acquire_connection(self, client_name: str) -> None:
        print(f"[{client_name}] Очікує на з'єднання")
        self._semaphore.acquire()
        with self._lock:
            self.active_connections += 1
            self.peak_connections = max(self.peak_connections, self.active_connections)
            print(f"[{client_name}] З'єднання отримано, активних: {self.active_connections}")

    def release_connection(self, client_name: str) -> None:
        with self._lock:
            self.active_connections -= 1
            self.total_served += 1
            print(f"[{client_name}] З'єднання звільнено, активних: {self.active_connections}")
        self._semaphore.release()

    def get_stats(self) -> dict:
        with self._lock:
            return {
                "max": self.max_connections,
                "active": self.active_connections,
                "total_served": self.total_served,
                "peak": self.peak_connections,
            }


def client_task(pool: ConnectionPool, client_name: str, ready_event: threading.Event) -> None:
    ready_event.wait()
    pool.acquire_connection(client_name)
    try:
        work_time = random.uniform(0.2, 0.5)
        print(f"[{client_name}] Працює {work_time:.1f} сек")
        time.sleep(work_time)
    finally:
        pool.release_connection(client_name)


def main():
    pool = ConnectionPool(max_connections=3)
    ready_event = threading.Event()
    threads = []

    for i in range(10):
        thread = threading.Thread(
            target=client_task,
            args=(pool, f"Client-{i:02d}", ready_event),
        )
        threads.append(thread)
        thread.start()

    time.sleep(0.2)
    print("Сервер готовий, клієнти починають роботу")
    ready_event.set()

    for thread in threads:
        thread.join()

    stats = pool.get_stats()
    print("\n=== Статистика пулу ===")
    print(f"Максимум з'єднань: {stats['max']}")
    print(f"Активних після завершення: {stats['active']}")
    print(f"Обслуговано клієнтів: {stats['total_served']}")
    print(f"Пікове навантаження: {stats['peak']}")
    print(f"Ліміт не перевищено: {stats['peak'] <= stats['max']}")


if __name__ == "__main__":
    main()
