import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
from PyQt6.QtCore import Qt


class PersonalDataForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Форма ввода данных")
        self.setGeometry(100, 100, 400, 300)

        # Создание основного виджета и макета
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Поля ввода данных
        self.add_input_field("Фамилия", "Введите вашу фамилию")
        self.add_input_field("Имя", "Введите ваше имя")
        self.add_input_field("Отчество", "Введите ваше отчество")
        self.add_input_field("Телефон", "Введите ваш телефон")

        # Кнопка для отправки данных
        self.submit_button = QPushButton("Отправить")
        self.submit_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.submit_button)

    def add_input_field(self, label_text, placeholder_text):
        """Добавляет поле ввода с меткой"""
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(label)

        entry = QLineEdit()
        entry.setPlaceholderText(placeholder_text)
        self.layout.addWidget(entry)

        # Сохраняем ссылки на поля ввода в объекте
        setattr(self, f"{label_text.lower()}_entry", entry)

    def submit_data(self):
        """Обработка нажатия кнопки 'Отправить'"""
        surname = self.фамилия_entry.text()
        name = self.имя_entry.text()
        patronymic = self.отчество_entry.text()
        phone = self.телефон_entry.text()

        print(f"Фамилия: {surname}")
        print(f"Имя: {name}")
        print(f"Отчество: {patronymic}")
        print(f"Телефон: {phone}")


# Основная точка входа в приложение
def main():
    app = QApplication(sys.argv)
    personal_form = PersonalDataForm()
    personal_form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
