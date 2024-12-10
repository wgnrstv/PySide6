import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QWidget,
)
from PyQt6.QtCore import Qt


class EngineControlForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление основными двигателями")
        self.setGeometry(100, 100, 600, 300)

        # Создание основного виджета и макета
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Основной горизонтальный макет для всех двигателей
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Добавление элементов управления двигателями
        self.add_engine_control("Двигатель №1")
        self.add_engine_control("Двигатель №2")
        self.add_engine_control("Двигатель №3")
        self.add_engine_control("Двигатель №4")

        # Общая тяга
        self.add_engine_control("Общая тяга", is_total=True)

    def add_engine_control(self, label_text, is_total=False):
        """Добавление элемента управления двигателем"""
        engine_layout = QVBoxLayout()

        # Ползунок для управления
        slider = QSlider(Qt.Orientation.Vertical)
        slider.setRange(0, 100)
        slider.setValue(50)  # Установим значение по умолчанию
        slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.setTickInterval(10)

        if is_total:
            slider.setEnabled(True)  # Ползунок общей тяги заблокирован для редактирования

        engine_layout.addWidget(slider)

        # Метка для двигателя
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        engine_layout.addWidget(label)

        self.layout.addLayout(engine_layout)


# Основная точка входа в приложение
def main():
    app = QApplication(sys.argv)
    engine_form = EngineControlForm()
    engine_form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
