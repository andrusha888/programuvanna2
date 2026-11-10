import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QComboBox, QCheckBox, QRadioButton, QSlider, QSpinBox,
    QProgressBar, QVBoxLayout, QHBoxLayout, QFormLayout
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анкета користувача")
        self.setMinimumSize(640, 500)

        title = QLabel("Заповнення анкети")
        title.setToolTip("Форма для введення основних даних")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Введіть ім'я")

        self.about = QTextEdit()
        self.about.setPlaceholderText("Коротко розкажіть про себе")
        self.about.setMaximumHeight(90)

        self.city = QComboBox()
        self.city.addItems(["Київ", "Львів", "Одеса", "Харків"])
        self.city.setCurrentIndex(1)

        self.age = QSpinBox()
        self.age.setRange(14, 100)
        self.age.setValue(20)

        self.agree = QCheckBox("Погоджуюся з обробкою даних")
        self.agree.setChecked(True)

        self.radio = QRadioButton("Отримувати повідомлення")
        self.radio.setChecked(True)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(40)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(40)
        self.slider.valueChanged.connect(self.progress.setValue)

        self.button = QPushButton("Показати дані")
        self.button.setToolTip("Вивести короткий підсумок анкети")
        self.result = QLabel("Результат з'явиться тут")
        self.result.setWordWrap(True)
        self.button.clicked.connect(self.show_data)

        form = QFormLayout()
        form.addRow("Ім'я:", self.name)
        form.addRow("Місто:", self.city)
        form.addRow("Вік:", self.age)
        form.addRow("Про себе:", self.about)

        choices = QHBoxLayout()
        choices.addWidget(self.agree)
        choices.addWidget(self.radio)

        level = QHBoxLayout()
        level_label = QLabel("Рівень:")
        level_label.setToolTip("Значення від 0 до 100")
        level.addWidget(level_label)
        level.addWidget(self.slider)
        level.addWidget(self.progress)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(choices)
        layout.addLayout(level)
        layout.addWidget(self.button)
        layout.addWidget(self.result)

    def show_data(self):
        name = self.name.text().strip() or "Не вказано"
        self.result.setText(
            f"Ім'я: {name}, місто: {self.city.currentText()}, "
            f"вік: {self.age.value()}, рівень: {self.slider.value()}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
