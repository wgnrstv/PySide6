from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Вызов метода для инициализации интерфейса
        self.initUi()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """

        # Создаём виджеты
        labelLogin = QtWidgets.QLabel("Логин")  # QLabel с текстом "Логин"
        labelRegistration = QtWidgets.QLabel("Пароль")  # QLabel с текстом "Пароль"

        self.lineEditLogin = QtWidgets.QLineEdit()  # Создаём виджет QLineEdit для логина
        self.lineEditLogin.setPlaceholderText("Введите логин")  # Добавляем placeholderText

        self.lineEditPassword = QtWidgets.QLineEdit()  # Создаём виджет QLineEdit для пароля
        self.lineEditPassword.setPlaceholderText("Введите пароль")  # Добавляем placeholderText
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  # Ограничиваем видимость вводимых знаков

        self.pushButtonLogin = QtWidgets.QPushButton()  # Создаём кнопку QPushButton
        self.pushButtonLogin.setText("Войти")  # Устанавливаем текст кнопки

        self.pushButtonRegistration = QtWidgets.QPushButton()  # Создаём кнопку QPushButton
        self.pushButtonRegistration.setText("Регистрация")  # Устанавливаем текст кнопки

        # Создаём макеты
        layoutLogin = QtWidgets.QHBoxLayout()  # Создаём QHBoxLayout для логина
        layoutLogin.addWidget(labelLogin)  # Добавляем метку "Логин"
        layoutLogin.addWidget(self.lineEditLogin)  # Добавляем поле ввода логина

        layoutPassword = QtWidgets.QHBoxLayout()  # Создаём QHBoxLayout для пароля
        layoutPassword.addWidget(labelRegistration)  # Добавляем метку "Пароль"
        layoutPassword.addWidget(self.lineEditPassword)  # Добавляем поле ввода пароля

        layoutButtons = QtWidgets.QHBoxLayout()  # Создаём QHBoxLayout для кнопок
        layoutButtons.addWidget(self.pushButtonLogin)  # Добавляем кнопку "Войти"
        layoutButtons.addWidget(self.pushButtonRegistration)  # Добавляем кнопку "Регистрация"

        layoutMain = QtWidgets.QVBoxLayout()  # Создаём QVBoxLayout для основного макета
        layoutMain.addLayout(layoutLogin)  # Добавляем макет логина
        layoutMain.addLayout(layoutPassword)  # Добавляем макет пароля
        layoutMain.addLayout(layoutButtons)  # Добавляем макет кнопок

        self.setLayout(layoutMain)  # Устанавливаем основной макет на виджет


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
