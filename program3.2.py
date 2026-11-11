from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable):
        self._listeners.setdefault(event, []).append(callback)

    def off(self, event: str, callback: Callable):
        if event in self._listeners and callback in self._listeners[event]:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        raise NotImplementedError


class SortByPriority(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda task: task.priority)


class SortByDeadline(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda task: task.deadline)


class SortByCreationDate(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda task: task.created_at, reverse=True)


@dataclass
class Task:
    title: str
    priority: int
    deadline: datetime
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


class TaskModel(EventEmitter):
    def __init__(self):
        super().__init__()
        self._tasks: list[Task] = []

    def add_task(self, title: str, priority: int, deadline: datetime):
        if not title.strip() or not 1 <= priority <= 5:
            raise ValueError("Потрібна назва та пріоритет від 1 до 5")
        task = Task(title, priority, deadline)
        self._tasks.append(task)
        self.emit("task_added", task)

    def complete_task(self, index: int):
        task = self._tasks[index]
        task.completed = True
        self.emit("task_completed", task)

    def remove_task(self, index: int):
        task = self._tasks.pop(index)
        self.emit("task_removed", task)

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        if include_completed:
            return self._tasks[:]
        return [task for task in self._tasks if not task.completed]

    def get_statistics(self) -> dict:
        total = len(self._tasks)
        completed = sum(task.completed for task in self._tasks)
        return {"Всього": total, "Виконано": completed, "Активних": total - completed}


class TaskView:
    def show_tasks(self, tasks: list[Task], title: str = "Завдання"):
        print(f"\n{title}:")
        print(f"{'№':<4}{'Назва':<24}{'Пріоритет':<12}{'Дедлайн':<14}Статус")
        for index, task in enumerate(tasks, 1):
            status = "Виконано" if task.completed else "Активне"
            print(f"{index:<4}{task.title:<24}{task.priority:<12}{task.deadline:%d.%m.%Y}    {status}")

    def show_message(self, message: str):
        print("[INFO]", message)

    def show_statistics(self, stats: dict):
        print("\nСтатистика:")
        for name, value in stats.items():
            print(f"  {name}: {value}")


class TaskController:
    def __init__(self, model: TaskModel, view: TaskView):
        self._model = model
        self._view = view
        self._sort_strategy: SortStrategy = SortByPriority()
        self._model.on("task_added", lambda task: self._view.show_message(f"Додано: {task.title}"))
        self._model.on("task_completed", lambda task: self._view.show_message(f"Виконано: {task.title}"))
        self._model.on("task_removed", lambda task: self._view.show_message(f"Видалено: {task.title}"))

    def set_sort_strategy(self, strategy: SortStrategy):
        self._sort_strategy = strategy

    def add_task(self, title: str, priority: int, deadline: datetime):
        self._model.add_task(title, priority, deadline)

    def complete_task(self, index: int):
        self._model.complete_task(index)

    def remove_task(self, index: int):
        self._model.remove_task(index)

    def show_all(self):
        tasks = self._sort_strategy.sort(self._model.get_tasks())
        self._view.show_tasks(tasks)

    def show_active(self):
        tasks = self._sort_strategy.sort(self._model.get_tasks(include_completed=False))
        self._view.show_tasks(tasks, title="Активні завдання")

    def show_stats(self):
        self._view.show_statistics(self._model.get_statistics())


def main():
    model = TaskModel()
    view = TaskView()
    ctrl = TaskController(model, view)

    ctrl.add_task("Вивчити Python", 2, datetime(2026, 11, 20))
    ctrl.add_task("Здати звіт", 1, datetime(2026, 11, 15))
    ctrl.add_task("Прочитати лекцію", 4, datetime(2026, 11, 13))
    ctrl.add_task("Зробити презентацію", 3, datetime(2026, 11, 25))
    ctrl.add_task("Повторити тести", 2, datetime(2026, 11, 18))

    print("\nСортування за пріоритетом:")
    ctrl.show_all()

    print("\nСортування за дедлайном:")
    ctrl.set_sort_strategy(SortByDeadline())
    ctrl.show_all()

    print("\nСортування за датою створення:")
    ctrl.set_sort_strategy(SortByCreationDate())
    ctrl.show_all()

    ctrl.complete_task(1)
    ctrl.show_active()
    ctrl.remove_task(2)
    ctrl.show_stats()


if __name__ == "__main__":
    main()
