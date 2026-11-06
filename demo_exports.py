import data_app
from data_app import *

print("Імпортовані через * імена:")
print([name for name in data_app.__all__ if name in globals()])
print("summarize є в пакеті:", hasattr(data_app, "summarize"))
print("summarize імпортовано через *:", "summarize" in globals())
