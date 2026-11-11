import json
from abc import ABC, abstractmethod
from datetime import datetime


class SingletonMeta(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LogFormatter(ABC):
    @abstractmethod
    def format(self, level: str, message: str, timestamp: datetime) -> str:
        raise NotImplementedError


class PlainFormatter(LogFormatter):
    def format(self, level: str, message: str, timestamp: datetime) -> str:
        return f"[{level}] {timestamp:%H:%M:%S} - {message}"


class JSONFormatter(LogFormatter):
    def format(self, level: str, message: str, timestamp: datetime) -> str:
        return json.dumps({"level": level, "time": timestamp.isoformat(), "message": message}, ensure_ascii=False)


class ColorFormatter(LogFormatter):
    COLORS = {"DEBUG": "\033[90m", "INFO": "\033[92m", "WARNING": "\033[93m", "ERROR": "\033[91m"}
    RESET = "\033[0m"

    def format(self, level: str, message: str, timestamp: datetime) -> str:
        return f"{self.COLORS[level]}[{level}] {timestamp:%H:%M:%S} - {message}{self.RESET}"


class FormatterFactory:
    _formatters: dict[str, type[LogFormatter]] = {
        "plain": PlainFormatter,
        "json": JSONFormatter,
        "color": ColorFormatter,
    }

    @classmethod
    def register(cls, name: str, formatter_cls: type[LogFormatter]):
        if not issubclass(formatter_cls, LogFormatter):
            raise TypeError("Форматер повинен наслідувати LogFormatter")
        cls._formatters[name] = formatter_cls

    @classmethod
    def create(cls, name: str) -> LogFormatter:
        if name not in cls._formatters:
            raise ValueError(f"Невідомий форматер: {name}")
        return cls._formatters[name]()

    @classmethod
    def available(cls) -> list[str]:
        return list(cls._formatters)


class Logger(metaclass=SingletonMeta):
    LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

    def __init__(self, formatter_name: str = "plain", min_level: str = "DEBUG"):
        if min_level not in self.LEVELS:
            raise ValueError("Невідомий рівень логування")
        self._formatter = FormatterFactory.create(formatter_name)
        self._min_level = min_level
        self._log_history: list[str] = []

    def set_formatter(self, name: str):
        self._formatter = FormatterFactory.create(name)

    def log(self, level: str, message: str):
        if level not in self.LEVELS:
            raise ValueError("Невідомий рівень логування")
        if self.LEVELS[level] < self.LEVELS[self._min_level]:
            return
        formatted = self._formatter.format(level, message, datetime.now())
        print(formatted)
        self._log_history.append(formatted)

    def debug(self, msg: str):
        self.log("DEBUG", msg)

    def info(self, msg: str):
        self.log("INFO", msg)

    def warning(self, msg: str):
        self.log("WARNING", msg)

    def error(self, msg: str):
        self.log("ERROR", msg)

    def get_history(self) -> list[str]:
        return self._log_history[:]


class ShortFormatter(LogFormatter):
    def format(self, level: str, message: str, timestamp: datetime) -> str:
        return f"{level}: {message}"


def main():
    logger1 = Logger("plain", "DEBUG")
    logger2 = Logger("json", "INFO")
    print("Singleton:", logger1 is logger2)

    logger1.info("Система запущена")
    logger1.warning("Мало пам'яті")
    logger1.error("Помилка з'єднання")

    logger1.set_formatter("json")
    logger1.debug("Діагностика")

    logger1.set_formatter("color")
    logger1.info("Кольоровий формат")

    FormatterFactory.register("short", ShortFormatter)
    logger1.set_formatter("short")
    logger1.info("Новий форматер")

    print("Форматери:", FormatterFactory.available())
    print("Історія:", len(logger1.get_history()), "записів")


if __name__ == "__main__":
    main()
