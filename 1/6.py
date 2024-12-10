import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QMessageBox,
)
from PyQt6.QtCore import Qt


class CalculatorForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 100, 400, 300)

        # Создание основного виджета и макета
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Поля ввода чисел
        self.add_number_input("Первое число:")
        self.add_number_input("Второе число:")

        # Кнопки операций
        self.add_operation_buttons()

        # Поле вывода результата
        self.result_label = QLabel("Результат: 0")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
        self.layout.addWidget(self.result_label)

    def add_number_input(self, label_text):
        """Добавляет поле ввода с меткой"""
        label = QLabel(label_text)
        self.layout.addWidget(label)

        entry = QLineEdit()
        entry.setPlaceholderText("Введите число")
        entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(entry)

        # Сохраняем ссылки на поля ввода
        setattr(self, f"{label_text.split()[0].lower()}_entry", entry)

    def add_operation_buttons(self):
        """Добавляет кнопки для операций"""
        button_layout = QHBoxLayout()

        buttons = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
        }

        for symbol, method in buttons.items():
            button = QPushButton(symbol)
            button.clicked.connect(method)
            button_layout.addWidget(button)

        self.layout.addLayout(button_layout)

    def get_numbers(self):
        """Получает значения из полей ввода и преобразует их в числа"""
        try:
            num1 = float(self.первое_entry.text())
            num2 = float(self.второе_entry.text())
            return num1, num2
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Введите оба числа в правильном формате!")
            return None, None

    def add(self):
        num1, num2 = self.get_numbers()
        if num1 is not None and num2 is not None:
            result = num1 + num2
            self.display_result(result)

    def subtract(self):
        num1, num2 = self.get_numbers()
        if num1 is not None and num2 is not None:
            result = num1 - num2
            self.display_result(result)

    def multiply(self):
        num1, num2 = self.get_numbers()
        if num1 is not None and num2 is not None:
            result = num1 * num2
            self.display_result(result)

    def divide(self):
        num1, num2 = self.get_numbers()
        if num2 == 0:
            QMessageBox.warning(self, "Ошибка деления", "На ноль делить нельзя!")
            return
        if num1 is not None and num2 is not None:
            result = num1 / num2
            self.display_result(result)

    def display_result(self, result):
        """Отображает результат операции"""
        self.result_label.setText(f"Результат: {result}")


# Основная точка входа в приложение
def main():
    app = QApplication(sys.argv)
    calculator_form = CalculatorForm()
    calculator_form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
