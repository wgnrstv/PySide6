from PySide6 import QtWidgets
from b import SystemInfoWidget
from c import WeatherWidget


class CombinedWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        """
        Инициализация интерфейса.
        """
        self.setWindowTitle("Системная информация и Погода")
        self.setGeometry(100, 100, 800, 600)

        # Создаем виджеты
        self.system_info_widget = SystemInfoWidget()
        self.weather_widget = WeatherWidget()

        # Компоновка
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.system_info_widget)
        layout.addWidget(self.weather_widget)

        self.setLayout(layout)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = CombinedWidget()
    window.show()
    sys.exit(app.exec())
