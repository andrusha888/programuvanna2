import threading
import time


def download_simulation(file_name: str, size_mb: float) -> dict:
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] Початок завантаження {file_name} ({size_mb} MB)")
    time.sleep(size_mb * 0.3)
    print(f"[{thread_name}] Завершено: {file_name}")
    return {"file": file_name, "size": size_mb, "thread": thread_name}


class MonitorThread(threading.Thread):
    def __init__(self, interval: float = 0.3):
        super().__init__(name="Monitor", daemon=True)
        self.interval = interval
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.wait(self.interval):
            print(f"[Monitor] Активних потоків: {threading.active_count()}")

    def stop(self):
        self._stop_event.set()


def main():
    files = [
        ("data.csv", 2.5),
        ("report.pdf", 1.0),
        ("image.png", 0.5),
        ("archive.zip", 4.0),
        ("log.txt", 0.3),
    ]

    monitor = MonitorThread()
    monitor.start()

    threads = []
    for index, (name, size) in enumerate(files, 1):
        thread = threading.Thread(
            target=download_simulation,
            args=(name, size),
            name=f"Download-{index}",
        )
        threads.append(thread)

    print("=== Паралельне виконання ===")
    start = time.perf_counter()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    parallel_time = time.perf_counter() - start

    monitor.stop()
    monitor.join()

    print("\n=== Послідовне виконання ===")
    start = time.perf_counter()
    for name, size in files:
        download_simulation(name, size)
    sequential_time = time.perf_counter() - start

    print(f"\nПаралельно: {parallel_time:.2f} сек")
    print(f"Послідовно: {sequential_time:.2f} сек")
    print(f"Прискорення: {sequential_time / parallel_time:.2f}x")


if __name__ == "__main__":
    main()
