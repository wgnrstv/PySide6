from PySide6 import QtWidgets, QtCore, QtGui
import datetime


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        """
        Инициализация интерфейса.
        """
        self.setWindowTitle("Проверка состояния окна")
        self.setGeometry(100, 100, 800, 600)

        # Создание виджетов
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setPlaceholderText("Лог событий...")
        self.plainTextEdit.setReadOnly(True)

        self.moveButton = QtWidgets.QPushButton("Переместить окно")
        self.screenInfoButton = QtWidgets.QPushButton("Получить параметры экрана")

        # Основной макет
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.plainTextEdit)
        layout.addWidget(self.moveButton)
        layout.addWidget(self.screenInfoButton)

        self.setLayout(layout)

    def init_signals(self):
        """
        Инициализация сигналов и слотов.
        """
        self.moveButton.clicked.connect(self.move_window)
        self.screenInfoButton.clicked.connect(self.get_screen_info)

        # Отслеживание событий перемещения и изменения размеров
        self.installEventFilter(self)

    def log_message(self, message: str):
        """
        Записывает сообщение в plainTextEdit с отметкой времени.
        """
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        self.plainTextEdit.appendPlainText(f"{timestamp} {message}")

    def move_window(self):
        """
        Перемещает окно в случайное место.
        """
        old_position = self.pos()
        new_position = QtCore.QPoint(
            old_position.x() + 50,
            old_position.y() + 50
        )
        self.move(new_position)
        self.log_message(f"Окно перемещено: старое положение {old_position}, новое положение {new_position}")

    def get_screen_info(self):
        """
        Получает параметры экрана и выводит в plainTextEdit.
        """
        screens = QtGui.QGuiApplication.screens()
        primary_screen = QtGui.QGuiApplication.primaryScreen()
        window_screen = primary_screen

        current_geometry = self.geometry()
        center_position = self.frameGeometry().center()

        info = [
            f"Количество экранов: {len(screens)}",
            f"Текущее основное окно: {primary_screen.name()}",
            f"Разрешение экрана: {primary_screen.size().width()}x{primary_screen.size().height()}",
            f"На каком экране окно находится: {window_screen.name()}",
            f"Размеры окна: {current_geometry.width()}x{current_geometry.height()}",
            f"Минимальные размеры окна: {self.minimumSize().width()}x{self.minimumSize().height()}",
            f"Текущее положение окна: {current_geometry.x()}, {current_geometry.y()}",
            f"Координаты центра приложения: {center_position.x()}, {center_position.y()}",
        ]

        for line in info:
            self.log_message(line)

    def eventFilter(self, obj, event):
        """
        Фильтрует события перемещения и изменения размеров окна.
        """
        if event.type() == QtCore.QEvent.Type.Move:
            old_position = event.oldPos() if hasattr(event, 'oldPos') else "?"
            self.log_message(f"Окно перемещено: старое положение {old_position}, новое положение {self.pos()}")
            print(f"[{datetime.datetime.now()}] Перемещение окна: {self.pos()}")

        elif event.type() == QtCore.QEvent.Type.Resize:
            self.log_message(f"Изменен размер окна: {self.size()}")
            print(f"[{datetime.datetime.now()}] Новый размер окна: {self.size()}")

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
