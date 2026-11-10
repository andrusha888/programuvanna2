import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QSpinBox, QComboBox,
    QCheckBox, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout
)


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Інтерактивна реєстрація")
        self.setMinimumSize(480, 360)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Ваше ім'я")

        self.age = QSpinBox()
        self.age.setRange(0, 100)
        self.age.setValue(0)

        self.course = QComboBox()
        self.course.addItems(["Оберіть курс", "Python", "Web", "Мережі"])

        self.agree = QCheckBox("Підтверджую правильність даних")
        self.preview = QLabel("Ім'я: не введено")
        self.age_label = QLabel("Вік: 0")
        self.course_label = QLabel("Курс: не обрано")
        self.result = QLabel("Заповніть форму")
        self.result.setWordWrap(True)

        self.submit = QPushButton("Підтвердити")
        self.submit.setEnabled(False)
        self.reset = QPushButton("Скинути")

        self.name.textChanged.connect(self.update_preview)
        self.age.valueChanged.connect(lambda value: self.age_label.setText(f"Вік: {value}"))
        self.course.currentTextChanged.connect(
            lambda text: self.course_label.setText(f"Курс: {text}")
        )
        self.agree.toggled.connect(self.submit.setEnabled)
        self.submit.clicked.connect(self.confirm)
        self.reset.clicked.connect(self.reset_form)

        form = QFormLayout()
        form.addRow("Ім'я:", self.name)
        form.addRow("Вік:", self.age)
        form.addRow("Курс:", self.course)

        buttons = QHBoxLayout()
        buttons.addWidget(self.submit)
        buttons.addWidget(self.reset)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.agree)
        layout.addWidget(self.preview)
        layout.addWidget(self.age_label)
        layout.addWidget(self.course_label)
        layout.addLayout(buttons)
        layout.addWidget(self.result)

    def update_preview(self, text):
        self.preview.setText(f"Ім'я: {text.strip() or 'не введено'}")

    def validate(self):
        if not self.name.text().strip():
            return "Введіть ім'я"
        if self.age.value() < 16:
            return "Вік повинен бути не менше 16 років"
        if self.course.currentIndex() == 0:
            return "Оберіть курс"
        if not self.agree.isChecked():
            return "Потрібно підтвердити правильність даних"
        return ""

    def confirm(self):
        error = self.validate()
        if error:
            self.result.setText("Помилка: " + error)
        else:
            self.result.setText(
                f"Успішно! {self.name.text().strip()}, "
                f"{self.age.value()} років, курс: {self.course.currentText()}"
            )

    def reset_form(self):
        self.name.clear()
        self.age.setValue(0)
        self.course.setCurrentIndex(0)
        self.agree.setChecked(False)
        self.result.setText("Заповніть форму")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec())
