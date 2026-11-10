import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QDialog, QDialogButtonBox, QVBoxLayout,
    QFormLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox,
    QPushButton, QListWidget, QMessageBox, QInputDialog
)


QSS = """
QWidget {
    background-color: #f3f6fb;
    color: #24334b;
    font-size: 14px;
}
QLabel {
    font-weight: 500;
}
QPushButton {
    background-color: #3266cf;
    color: white;
    padding: 9px;
    border: none;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #244f9e;
}
QPushButton:pressed {
    background-color: #173871;
}
QLineEdit, QSpinBox, QListWidget {
    background-color: white;
    color: #24334b;
    border: 1px solid #a7b7cf;
    border-radius: 5px;
    padding: 5px;
}
QLineEdit:focus, QSpinBox:focus {
    border: 2px solid #3266cf;
}
QLabel#mainTitle {
    color: #16449d;
    font-size: 24px;
    font-weight: bold;
}
"""


class ContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новий контакт")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Ім'я контакту")
        self.city = QLineEdit()
        self.city.setPlaceholderText("Місто")
        self.age = QSpinBox()
        self.age.setRange(1, 100)
        self.age.setValue(18)

        form = QFormLayout()
        form.addRow("Ім'я:", self.name)
        form.addRow("Місто:", self.city)
        form.addRow("Вік:", self.age)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def save(self):
        if not self.name.text().strip() or not self.city.text().strip():
            QMessageBox.warning(self, "Помилка", "Заповніть ім'я та місто")
            return
        self.accept()

    def get_data(self):
        return self.name.text().strip(), self.city.text().strip(), self.age.value()


class ContactsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список контактів")
        self.setMinimumSize(560, 400)
        self.styled = False

        self.title = QLabel("Мої контакти")
        self.title.setObjectName("mainTitle")
        self.contacts = QListWidget()
        self.status = QLabel("Стиль вимкнено. Контактів: 0")

        add_button = QPushButton("Додати контакт")
        rename_button = QPushButton("Змінити назву")
        clear_button = QPushButton("Очистити список")
        self.style_button = QPushButton("Увімкнути стиль")

        add_button.clicked.connect(self.add_contact)
        rename_button.clicked.connect(self.rename_list)
        clear_button.clicked.connect(self.clear_contacts)
        self.style_button.clicked.connect(self.toggle_style)

        buttons = QHBoxLayout()
        buttons.addWidget(add_button)
        buttons.addWidget(rename_button)
        buttons.addWidget(clear_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.contacts)
        layout.addLayout(buttons)
        layout.addWidget(self.style_button)
        layout.addWidget(self.status)

    def add_contact(self):
        dialog = ContactDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, city, age = dialog.get_data()
            self.contacts.addItem(f"{name} | {city} | {age} років")
            self.status.setText(f"Контакт додано. Усього: {self.contacts.count()}")

    def rename_list(self):
        title, ok = QInputDialog.getText(self, "Нова назва", "Введіть назву списку:")
        if ok and title.strip():
            self.title.setText(title.strip())
            self.status.setText("Назву списку змінено")

    def clear_contacts(self):
        answer = QMessageBox.question(
            self, "Підтвердження", "Видалити всі контакти?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.contacts.clear()
            self.status.setText("Список очищено. Контактів: 0")
        else:
            self.status.setText("Очищення скасовано")

    def toggle_style(self):
        self.styled = not self.styled
        QApplication.instance().setStyleSheet(QSS if self.styled else "")
        self.style_button.setText("Вимкнути стиль" if self.styled else "Увімкнути стиль")
        self.status.setText("Стиль увімкнено" if self.styled else "Стиль вимкнено")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactsWindow()
    window.show()
    sys.exit(app.exec())
