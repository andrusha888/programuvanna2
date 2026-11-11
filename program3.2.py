import queue
import random
import threading
import time


class Task:
    def __init__(self, task_id: int, data: str, priority: int = 0):
        self.task_id = task_id
        self.data = data
        self.priority = priority
        self.created_at = time.time()

    def __repr__(self):
        return f"Task(id={self.task_id}, data={self.data!r})"


def producer(task_queue: queue.Queue, num_tasks: int, producer_id: int) -> None:
    for i in range(num_tasks):
        task = Task(
            task_id=producer_id * 100 + i,
            data=f"Дані від виробника {producer_id}, пакет {i}",
            priority=random.randint(1, 5),
        )
        task_queue.put(task)
        print(f"[Виробник-{producer_id}] Створено {task.task_id}")
        time.sleep(random.uniform(0.02, 0.06))


def consumer(task_queue: queue.Queue, consumer_id: int,
             results: list, results_lock: threading.Lock) -> None:
    while True:
        try:
            task = task_queue.get(timeout=2)
        except queue.Empty:
            print(f"[Споживач-{consumer_id}] Черга порожня")
            break

        try:
            if task is None:
                print(f"[Споживач-{consumer_id}] Завершення")
                break
            start = time.perf_counter()
            time.sleep(random.uniform(0.05, 0.12))
            elapsed = time.perf_counter() - start
            with results_lock:
                results.append((task.task_id, elapsed))
            print(f"[Споживач-{consumer_id}] Оброблено {task.task_id}")
        finally:
            task_queue.task_done()


def producer_consumer_demo():
    task_queue = queue.Queue(maxsize=5)
    results = []
    results_lock = threading.Lock()
    producers = []
    consumers = []

    for i in range(3):
        thread = threading.Thread(
            target=consumer, args=(task_queue, i + 1, results, results_lock)
        )
        consumers.append(thread)
        thread.start()

    for i in range(2):
        thread = threading.Thread(target=producer, args=(task_queue, 5, i + 1))
        producers.append(thread)
        thread.start()

    for thread in producers:
        thread.join()

    for _ in consumers:
        task_queue.put(None)

    task_queue.join()
    for thread in consumers:
        thread.join()

    average = sum(elapsed for _, elapsed in results) / len(results)
    print(f"\nОброблено завдань: {len(results)}")
    print(f"Середній час обробки: {average:.3f} сек")


def deadlock_demo():
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    ready = threading.Barrier(2)
    detected = threading.Event()

    def worker_1():
        with lock_a:
            print("[Worker-1] Захопив Lock A")
            ready.wait()
            acquired = lock_b.acquire(timeout=0.6)
            if acquired:
                print("[Worker-1] Захопив Lock B")
                lock_b.release()
            else:
                print("[Worker-1] Виявлено потенційний дедлок")
                detected.set()

    def worker_2():
        with lock_b:
            print("[Worker-2] Захопив Lock B")
            ready.wait()
            acquired = lock_a.acquire(timeout=0.6)
            if acquired:
                print("[Worker-2] Захопив Lock A")
                lock_a.release()
            else:
                print("[Worker-2] Виявлено потенційний дедлок")
                detected.set()

    print("\n=== Потенційний дедлок ===")
    threads = [threading.Thread(target=worker_1), threading.Thread(target=worker_2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Дедлок виявлено: {detected.is_set()}")

    def safe_worker(name):
        with lock_a:
            with lock_b:
                print(f"[{name}] Обидва замки отримано в порядку A -> B")

    print("\n=== Безпечна версія ===")
    threads = [
        threading.Thread(target=safe_worker, args=("Safe-1",)),
        threading.Thread(target=safe_worker, args=("Safe-2",)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Безпечні потоки завершилися")


def main():
    print("=== Producer-Consumer ===")
    producer_consumer_demo()
    deadlock_demo()


if __name__ == "__main__":
    main()
