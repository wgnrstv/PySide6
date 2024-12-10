from PySide6 import QtWidgets, QtCore
from a import WeatherHandler


class WeatherWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.weather_thread = None
        self.init_ui()
        self.init_signals()

    def init_ui(self):
        """
        Инициализация интерфейса.
        """
        self.setWindowTitle("Погода")
        self.setGeometry(100, 100, 400, 300)

        # Поля для ввода широты и долготы
        self.lat_label = QtWidgets.QLabel("Широта:")
        self.lat_input = QtWidgets.QLineEdit()
        self.lat_input.setPlaceholderText("Введите широту")

        self.lon_label = QtWidgets.QLabel("Долгота:")
        self.lon_input = QtWidgets.QLineEdit()
        self.lon_input.setPlaceholderText("Введите долготу")

        # Поле для ввода времени задержки
        self.delay_label = QtWidgets.QLabel("Время задержки (сек):")
        self.delay_input = QtWidgets.QLineEdit()
        self.delay_input.setPlaceholderText("Введите время задержки")
        self.delay_input.setText("10")  # Значение по умолчанию

        # Поле для вывода информации о погоде
        self.weather_info_label = QtWidgets.QLabel("Информация о погоде:")
        self.weather_info_display = QtWidgets.QPlainTextEdit()
        self.weather_info_display.setReadOnly(True)

        # Кнопка для запуска/остановки потока
        self.toggle_button = QtWidgets.QPushButton("Запустить")

        # Компоновка
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.lat_label)
        layout.addWidget(self.lat_input)
        layout.addWidget(self.lon_label)
        layout.addWidget(self.lon_input)
        layout.addWidget(self.delay_label)
        layout.addWidget(self.delay_input)
        layout.addWidget(self.weather_info_label)
        layout.addWidget(self.weather_info_display)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)

    def init_signals(self):
        """
        Инициализация сигналов.
        """
        self.toggle_button.clicked.connect(self.toggle_thread)

    def toggle_thread(self):
        """
        Запускает или останавливает поток WeatherHandler.
        """
        if self.weather_thread is None:  # Запуск потока
            lat = self.lat_input.text()
            lon = self.lon_input.text()
            delay = self.delay_input.text()

            # Проверка на корректность входных данных
            try:
                lat = float(lat)
                lon = float(lon)
                delay = int(delay)
                if delay <= 0:
                    raise ValueError("Задержка должна быть больше 0.")
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка ввода", "Введите корректные данные.")
                return

            # Блокируем поля ввода
            self.lat_input.setDisabled(True)
            self.lon_input.setDisabled(True)
            self.delay_input.setDisabled(True)

            # Создаем и запускаем поток
            self.weather_thread = WeatherHandler(lat, lon)
            self.weather_thread.setDelay(delay)
            self.weather_thread.weatherDataReceived.connect(self.update_weather_info)
            self.weather_thread.weatherErrorOccurred.connect(self.handle_error)
            self.weather_thread.start()

            self.toggle_button.setText("Остановить")
        else:  # Остановка потока
            self.weather_thread.stop()
            self.weather_thread = None

            # Разблокируем поля ввода
            self.lat_input.setDisabled(False)
            self.lon_input.setDisabled(False)
            self.delay_input.setDisabled(False)

            self.toggle_button.setText("Запустить")

    def update_weather_info(self, data):
        """
        Обновляет информацию о погоде в поле вывода.

        :param data: Словарь с данными о погоде.
        """
        weather = data.get("current_weather", {})
        temperature = weather.get("temperature", "N/A")
        wind_speed = weather.get("windspeed", "N/A")
        weather_info = f"Температура: {temperature}°C\nСкорость ветра: {wind_speed} м/с"
        self.weather_info_display.setPlainText(weather_info)

    def handle_error(self, error_message):
        """
        Обрабатывает ошибки при работе с потоком.

        :param error_message: Текст ошибки.
        """
        QtWidgets.QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {error_message}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = WeatherWidget()
    widget.show()
    sys.exit(app.exec())
