import functools


def auto_repr(cls):
    parameters = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]

    def new_repr(self):
        values = ", ".join(f"{name}={getattr(self, name)!r}" for name in parameters)
        return f"{cls.__name__}({values})"

    cls.__repr__ = new_repr
    return cls


def frozen(cls):
    original_init = cls.__init__
    original_setattr = cls.__setattr__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        object.__setattr__(self, "_frozen", True)

    def new_setattr(self, name, value):
        if getattr(self, "_frozen", False):
            raise AttributeError(f"Атрибут {name} не можна змінити")
        original_setattr(self, name, value)

    cls.__init__ = new_init
    cls.__setattr__ = new_setattr
    return cls


def log_methods(cls):
    def make_wrapper(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            print(f"Виклик {method.__name__}{args}")
            try:
                result = method(self, *args, **kwargs)
            except Exception as error:
                print(f"Помилка {method.__name__}: {error}")
                raise
            print(f"Результат {method.__name__}: {result}")
            return result
        return wrapper

    for name, value in vars(cls).copy().items():
        if not name.startswith("_") and callable(value):
            setattr(cls, name, make_wrapper(value))
    return cls


@auto_repr
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@frozen
class ImmutableConfig:
    def __init__(self, host: str, port: int, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug


@log_methods
class MathService:
    def add(self, a: float, b: float) -> float:
        return a + b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Ділення на нуль")
        return a / b


@frozen
@auto_repr
@log_methods
class StudentRecord:
    def __init__(self, name: str, grade: int):
        self.name = name
        self.grade = grade

    def describe(self):
        return f"{self.name}: {self.grade} балів"


def main():
    p = Point(3.0, 4.0)
    print("Точка:", repr(p))
    print("Відстань до початку:", p.distance_to(Point(0.0, 0.0)))

    cfg = ImmutableConfig("localhost", 8080, debug=True)
    print("Конфігурація:", cfg.host, cfg.port, cfg.debug)
    try:
        cfg.host = "remote"
    except AttributeError as error:
        print("Очікувана помилка:", error)

    service = MathService()
    service.add(10, 20)
    service.multiply(3, 7)
    try:
        service.divide(10, 0)
    except ValueError:
        print("Помилку ділення перехоплено")

    print("\nКомбінація трьох декораторів:")
    record = StudentRecord("Олена", 95)
    print(repr(record))
    print(record.describe())
    try:
        record.grade = 100
    except AttributeError as error:
        print("Очікувана помилка:", error)


if __name__ == "__main__":
    main()
