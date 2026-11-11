from abc import abstractmethod


class PluginMeta(type):
    _registry: dict[str, type] = {}
    REQUIRED_ATTRS = ("name", "version")

    def __new__(mcs, cls_name: str, bases: tuple, namespace: dict):
        if bases:
            for attribute in mcs.REQUIRED_ATTRS:
                if attribute not in namespace or not namespace[attribute]:
                    raise TypeError(f"Плагін {cls_name} повинен мати атрибут {attribute}")
            if namespace["name"] in mcs._registry:
                raise TypeError(f"Плагін {namespace['name']} вже зареєстрований")

        cls = super().__new__(mcs, cls_name, bases, namespace)
        if bases:
            mcs._registry[cls.name] = cls
        return cls

    @classmethod
    def get_registry(mcs) -> dict[str, type]:
        return mcs._registry.copy()

    @classmethod
    def create_plugin(mcs, plugin_name: str):
        if plugin_name not in mcs._registry:
            raise ValueError(f"Плагін {plugin_name} не знайдено")
        return mcs._registry[plugin_name]()


class BasePlugin(metaclass=PluginMeta):
    @abstractmethod
    def execute(self, data: str) -> str:
        raise NotImplementedError


class UpperPlugin(BasePlugin):
    name = "upper"
    version = "1.0"

    def execute(self, data: str) -> str:
        return data.upper()


class ReversePlugin(BasePlugin):
    name = "reverse"
    version = "1.0"

    def execute(self, data: str) -> str:
        return data[::-1]


class CensorPlugin(BasePlugin):
    name = "censor"
    version = "1.1"

    def execute(self, data: str) -> str:
        for word in ("Світ", "секрет"):
            data = data.replace(word, "***")
        return data


def hash_execute(self, data: str) -> str:
    return str(hash(data))


HashPlugin = type(
    "HashPlugin",
    (BasePlugin,),
    {"name": "hash", "version": "2.0", "execute": hash_execute},
)


def main():
    print("Зареєстровані плагіни:")
    for name, cls in PluginMeta.get_registry().items():
        print(f"  {name} (v{cls.version}): {cls.__name__}")

    print("\nРезультати роботи плагінів:")
    test_data = "Привіт Світ"
    for name in PluginMeta.get_registry():
        plugin = PluginMeta.create_plugin(name)
        print(f"  {name}: {plugin.execute(test_data)}")

    print("\nПеревірка відсутнього атрибута:")
    try:
        class InvalidPlugin(BasePlugin):
            name = "invalid"

            def execute(self, data: str) -> str:
                return data
    except TypeError as error:
        print("Очікувана помилка:", error)


if __name__ == "__main__":
    main()
