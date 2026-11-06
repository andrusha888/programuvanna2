ЛАБОРАТОРНА РОБОТА: ВИКЛЮЧЕННЯ, МОДУЛІ, ДОКУМЕНТАЦІЯ

Для коректної роботи виконайте команди з цього каталогу:

python завдання_1.py
python завдання_2.py
python -m data_app
python demo_exports.py
python demo_docs.py

Завдання 1: завдання_1.py, обробка різних виключень.
Завдання 2: завдання_2.py, власні виключення та ланцюжки помилок.
Завдання 3: data_app, модульна структура та три форми імпорту.
Завдання 4: docstrings, анотації типів і demo_docs.py.

Структура каталогу:
requirements.txt       Перелік залежностей (їх немає).
sample_data.txt         Вхідний файл з числом 120.
demo_exports.py         Демонстрація дії __all__.
demo_docs.py            Інтроспекція: help, __doc__, __name__, __annotations__.
data_app/__init__.py    Публічні імена пакету і __all__.
data_app/__main__.py    Точка входу для python -m data_app.
data_app/core/__init__.py       Публічні імена підпакету core.
data_app/core/errors.py        Ієрархія власних виключень.
data_app/core/operations.py    Перетворення і обчислення.
data_app/utils/__init__.py      Публічні імена підпакету utils.
data_app/utils/storage.py      Читання текстових файлів.
data_app/utils/display.py      Виведення повідомлень.
