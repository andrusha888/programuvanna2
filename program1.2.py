class ValidatedField:
    def __init__(self, expected_type: type, min_value=None, max_value=None):
        self.expected_type = expected_type
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name)

    def __set__(self, obj, value):
        if type(value) is not self.expected_type:
            raise TypeError(f"Поле {self.name} повинно мати тип {self.expected_type.__name__}")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Поле {self.name} не може бути меншим за {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Поле {self.name} не може бути більшим за {self.max_value}")
        setattr(obj, self.storage_name, value)


class ConfigSection:
    _sections: dict[str, type] = {}

    def __init_subclass__(cls, section_name: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        if not section_name:
            raise ValueError("Потрібно вказати section_name")
        cls._sections[section_name] = cls

    @classmethod
    def get_section(cls, name: str):
        return cls._sections[name]

    @classmethod
    def list_sections(cls) -> list[str]:
        return list(cls._sections)


class DatabaseConfig(ConfigSection, section_name="database"):
    host = ValidatedField(str)
    port = ValidatedField(int, min_value=1, max_value=65535)
    max_connections = ValidatedField(int, min_value=1, max_value=1000)

    def __init__(self, host: str, port: int, max_connections: int):
        self.host = host
        self.port = port
        self.max_connections = max_connections


class LoggingConfig(ConfigSection, section_name="logging"):
    level = ValidatedField(str)
    max_file_size_mb = ValidatedField(int, min_value=1, max_value=1024)

    def __init__(self, level: str, max_file_size_mb: int):
        self.level = level
        self.max_file_size_mb = max_file_size_mb


def main():
    print("Зареєстровані секції:", ConfigSection.list_sections())

    db = ConfigSection.get_section("database")("localhost", 5432, 100)
    logs = ConfigSection.get_section("logging")("INFO", 50)
    print(f"База даних: {db.host}:{db.port}, з'єднань: {db.max_connections}")
    print(f"Логи: {logs.level}, максимальний розмір: {logs.max_file_size_mb} МБ")

    try:
        db.port = "5432"
    except TypeError as error:
        print("Помилка типу:", error)

    try:
        db.max_connections = 1500
    except ValueError as error:
        print("Помилка діапазону:", error)

    db.port = 3306
    print("Правильно змінений порт:", db.port)


if __name__ == "__main__":
    main()
