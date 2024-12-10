from PySide6 import QtWidgets, QtCore
from a import SystemInfo


class SystemInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()
        self.init_signals()
        self.start_system_info_thread()

    def init_ui(self):
        """
        Инициализация интерфейса.
        """
        self.setWindowTitle("Системная информация")
        self.setGeometry(100, 100, 400, 200)

        # Поле для ввода времени задержки
        self.delay_label = QtWidgets.QLabel("Время задержки (сек):")
        self.delay_input = QtWidgets.QLineEdit()
        self.delay_input.setPlaceholderText("Введите время задержки")
        self.delay_input.setText("1")  # Значение по умолчанию

        # Поля для вывода информации о загрузке CPU и RAM
        self.cpu_label = QtWidgets.QLabel("Загрузка CPU:")
        self.cpu_value = QtWidgets.QLabel("0%")

        self.ram_label = QtWidgets.QLabel("Загрузка RAM:")
        self.ram_value = QtWidgets.QLabel("0%")

        # Компоновка
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.delay_label)
        layout.addWidget(self.delay_input)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_value)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_value)

        self.setLayout(layout)

    def init_signals(self):
        """
        Инициализация сигналов.
        """
        # Сигнал изменения задержки
        self.delay_input.textChanged.connect(self.update_delay)

    def start_system_info_thread(self):
        """
        Создает и запускает поток SystemInfo.
        """
        self.system_info_thread = SystemInfo()
        self.system_info_thread.systemInfoReceived.connect(self.update_system_info)
        self.system_info_thread.start()

        # Устанавливаем задержку из поля ввода при старте
        self.update_delay(self.delay_input.text())

    def update_system_info(self, data):
        """
        Обновляет значения загрузки CPU и RAM на виджете.

        :param data: Список с данными о загрузке [CPU, RAM].
        """
        cpu, ram = data
        self.cpu_value.setText(f"{cpu}%")
        self.ram_value.setText(f"{ram}%")

    def update_delay(self, delay):
        """
        Обновляет время задержки в потоке.

        :param delay: Новое значение задержки.
        """
        try:
            delay = float(delay)
            if delay > 0:
                self.system_info_thread.delay = delay
        except ValueError:
            pass  # Игнорируем некорректные значения


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = SystemInfoWidget()
    widget.show()
    sys.exit(app.exec())
