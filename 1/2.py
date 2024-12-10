import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QGridLayout,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class ShipParametersForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Параметры корабля")
        self.setGeometry(100, 100, 400, 300)

        # Создание основного виджета и макета
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # Параметры
        self.add_parameter("Температура на борту", "22 C", 0)
        self.add_parameter("Разгерметизация", "Отсутствует", 1)
        self.add_parameter("Бак №1", "Норма", 2)
        self.add_parameter("Бак №2", "Норма", 3)
        self.add_parameter("Бак №3", "Норма", 4)

    def add_parameter(self, label_text, value_text, row):
        """Функция добавления строки параметров"""
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12))
        self.layout.addWidget(label, row, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        value = QLabel(value_text)
        value.setFont(QFont("Arial", 12))
        value.setStyleSheet("color: green;" if "Норма" in value_text or "Отсутствует" in value_text else "color: red;")
        self.layout.addWidget(value, row, 1, alignment=Qt.AlignmentFlag.AlignLeft)


# Основная точка входа в приложение
def main():
    app = QApplication(sys.argv)
    ship_form = ShipParametersForm()
    ship_form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
