import sys
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QSpinBox, QPushButton,
    QVBoxLayout, QHBoxLayout
)


class InputPanel(QWidget):
    text_sent = pyqtSignal(str)
    level_changed = pyqtSignal(int, str)
    reset_notice = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Введіть назву завдання")
        self.level = QSpinBox()
        self.level.setRange(1, 10)
        self.level.setValue(1)
        self.level_label = QLabel("Рівень у формі: 1")
        self.send = QPushButton("Надіслати текст")
        self.reset = QPushButton("Скинути рівень без сигналу")

        self.send.clicked.connect(self.send_text)
        self.level.valueChanged.connect(self.send_level)
        self.reset.clicked.connect(self.reset_level)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Компонент введення"))
        layout.addWidget(self.name)
        layout.addWidget(QLabel("Рівень складності:"))
        layout.addWidget(self.level)
        layout.addWidget(self.level_label)
        layout.addWidget(self.send)
        layout.addWidget(self.reset)

    def send_text(self):
        self.text_sent.emit(self.name.text().strip() or "Порожній текст")

    def send_level(self, value):
        self.level_label.setText(f"Рівень у формі: {value}")
        self.level_changed.emit(value, self.name.text().strip() or "Без назви")

    def reset_level(self):
        previous = self.level.blockSignals(True)
        self.level.setValue(1)
        self.level.blockSignals(previous)
        self.level_label.setText("Рівень у формі: 1")
        self.reset_notice.emit("Рівень скинуто без надсилання level_changed")


class ResultPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.text_label = QLabel("Отриманий текст: немає")
        self.level_label = QLabel("Останній отриманий рівень: немає")
        self.notice_label = QLabel("Змініть рівень на 5, а потім скиньте")
        self.text_label.setWordWrap(True)
        self.level_label.setWordWrap(True)
        self.notice_label.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Компонент результатів"))
        layout.addWidget(self.text_label)
        layout.addWidget(self.level_label)
        layout.addWidget(self.notice_label)

    def show_text(self, text):
        self.text_label.setText(f"Отриманий текст: {text}")

    def show_level(self, value, name):
        self.level_label.setText(f"Останній отриманий рівень: {value}, завдання: {name}")
        self.notice_label.setText("Сигнал рівня отримано")

    def show_notice(self, message):
        self.notice_label.setText(message)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Обмін даними через сигнали")
        self.setMinimumSize(650, 330)
        input_panel = InputPanel()
        result_panel = ResultPanel()

        input_panel.text_sent.connect(result_panel.show_text)
        input_panel.level_changed.connect(result_panel.show_level)
        input_panel.reset_notice.connect(result_panel.show_notice)

        layout = QHBoxLayout(self)
        layout.addWidget(input_panel)
        layout.addWidget(result_panel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
