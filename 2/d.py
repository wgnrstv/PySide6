from PySide6 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings("MyApp", "EventFilterSettings")
        self.init_ui()
        self.init_signals()
        self.load_settings()

    def init_ui(self):
        """
        Инициализация интерфейса
        """
        self.setWindowTitle("Взаимодействие виджетов")

        # Виджеты
        self.dial = QtWidgets.QDial()
        self.dial.setRange(0, 100)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)

        self.lcd = QtWidgets.QLCDNumber()

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(["Decimal", "Hexadecimal", "Octal", "Binary"])

        # Основной макет
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.dial)
        layout.addWidget(self.slider)
        layout.addWidget(self.lcd)
        layout.addWidget(self.comboBox)

        self.setLayout(layout)

    def init_signals(self):
        """
        Подключение сигналов и слотов
        """
        # Соединяем QDial, QSlider и QLCDNumber
        self.dial.valueChanged.connect(self.update_all_widgets)
        self.slider.valueChanged.connect(self.update_all_widgets)
        self.comboBox.currentIndexChanged.connect(self.update_lcd_format)

        # Фильтр событий для QDial (обработка нажатий клавиш)
        self.dial.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        Обработка событий для виджетов
        """
        if obj is self.dial and event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key_Plus:
                self.dial.setValue(self.dial.value() + 1)
                print(f"Dial: {self.dial.value()}")
            elif event.key() == QtCore.Qt.Key_Minus:
                self.dial.setValue(self.dial.value() - 1)
                print(f"Dial: {self.dial.value()}")
        return super().eventFilter(obj, event)

    def update_all_widgets(self, value):
        """
        Обновляет значения всех связанных виджетов
        """
        self.dial.blockSignals(True)
        self.slider.blockSignals(True)

        self.dial.setValue(value)
        self.slider.setValue(value)
        self.lcd.display(value)

        self.dial.blockSignals(False)
        self.slider.blockSignals(False)

    def update_lcd_format(self):
        """
        Обновляет формат отображения числа на QLCDNumber
        """
        mode = self.comboBox.currentText()
        value = self.dial.value()

        if mode == "Decimal":
            self.lcd.setDecMode()
            self.lcd.display(value)
        elif mode == "Hexadecimal":
            self.lcd.setHexMode()
            self.lcd.display(value)
        elif mode == "Octal":
            self.lcd.setOctMode()
            self.lcd.display(value)
        elif mode == "Binary":
            binary_value = bin(value)[2:]
            self.lcd.display(binary_value)

    def load_settings(self):
        """
        Загружает настройки из QSettings
        """
        mode = self.settings.value("displayMode", "Decimal")
        value = int(self.settings.value("lcdValue", 0))

        self.dial.setValue(value)
        self.comboBox.setCurrentText(mode)
        self.update_lcd_format()

    def closeEvent(self, event):
        """
        Сохраняет настройки перед закрытием программы
        """
        self.settings.setValue("displayMode", self.comboBox.currentText())
        self.settings.setValue("lcdValue", self.dial.value())
        super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
