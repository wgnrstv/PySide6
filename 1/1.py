import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Форма входа")
        self.setGeometry(100, 100, 300, 200)

        # Создание основного виджета и макета
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Поле для ввода логина
        self.login_label = QLabel("Login")
        self.layout.addWidget(self.login_label)

        self.login_entry = QLineEdit()
        self.layout.addWidget(self.login_entry)

        # Поле для ввода пароля
        self.password_label = QLabel("Password")
        self.layout.addWidget(self.password_label)

        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)  # Скрытие пароля
        self.layout.addWidget(self.password_entry)

        # Кнопка "Войти"
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login_action)
        self.layout.addWidget(self.login_button)

    def login_action(self):
        login = self.login_entry.text()
        password = self.password_entry.text()
        print(f"Login: {login}, Password: {password}")  # Вывод логина и пароля в консоль


def main():
    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
