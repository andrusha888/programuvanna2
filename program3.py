import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox, QToolBar
)


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовий редактор")
        self.setMinimumSize(650, 450)
        self.filename = ""

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Введіть текст або відкрийте файл")
        self.setCentralWidget(self.editor)

        open_action = QAction("Відкрити", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Зберегти", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)

        exit_action = QAction("Вийти", self)
        exit_action.triggered.connect(self.close)

        about_action = QAction("Про програму", self)
        about_action.triggered.connect(self.show_about)

        help_action = QAction("Підказка", self)
        help_action.triggered.connect(self.show_help)

        file_menu = self.menuBar().addMenu("Файл")
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        help_menu = self.menuBar().addMenu("Довідка")
        help_menu.addAction(about_action)
        help_menu.addAction(help_action)

        toolbar = QToolBar("Швидкі дії")
        self.addToolBar(toolbar)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)

        self.statusBar().showMessage("Готово до роботи")
        self.editor.textChanged.connect(self.update_status)

    def update_status(self):
        count = len(self.editor.toPlainText())
        self.statusBar().showMessage(f"Кількість символів: {count}")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Відкрити файл", "", "Текстові файли (*.txt);;Усі файли (*)"
        )
        if not path:
            self.statusBar().showMessage("Відкриття скасовано")
            return
        try:
            with open(path, "r", encoding="utf-8") as file:
                text = file.read()
        except (OSError, UnicodeError) as error:
            QMessageBox.warning(self, "Помилка", str(error))
            return
        self.editor.setPlainText(text)
        self.filename = path
        self.statusBar().showMessage(f"Відкрито: {path}")

    def save_file(self):
        path = self.filename
        if not path:
            path, _ = QFileDialog.getSaveFileName(
                self, "Зберегти файл", "текст.txt", "Текстові файли (*.txt)"
            )
        if not path:
            self.statusBar().showMessage("Збереження скасовано")
            return
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.editor.toPlainText())
        except OSError as error:
            QMessageBox.warning(self, "Помилка", str(error))
            return
        self.filename = path
        self.statusBar().showMessage(f"Збережено: {path}")

    def show_about(self):
        QMessageBox.about(self, "Про програму", "Простий текстовий редактор на PyQt6")
        self.statusBar().showMessage("Відкрито інформацію про програму")

    def show_help(self):
        QMessageBox.information(
            self, "Підказка", "Ctrl+O відкриває файл, Ctrl+S зберігає текст."
        )
        self.statusBar().showMessage("Підказку переглянуто")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec())
