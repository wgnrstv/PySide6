import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QWidget,
    QListWidget,
    QGroupBox,
    QButtonGroup,
    QMessageBox,
)


class BookSelectionForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор книги и способа оплаты")
        self.setGeometry(100, 100, 400, 400)

        # Основной виджет и макет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Секция: выбор книги
        self.add_book_selection()

        # Секция: выбор способа оплаты
        self.add_payment_selection()

        # Кнопка "Оплатить"
        self.pay_button = QPushButton("Оплатить")
        self.pay_button.clicked.connect(self.process_payment)
        self.layout.addWidget(self.pay_button)

    def add_book_selection(self):
        """Добавляет виджет выбора книги"""
        self.book_label = QLabel("Выберите книгу")
        self.book_label.setStyleSheet("font-weight: bold; font-size: 14px; color: magenta;")
        self.layout.addWidget(self.book_label)

        self.book_list = QListWidget()
        self.book_list.addItems([
            "Гарри Поттер и узник Азкабана — Джоан Роулинг",
            "Благословение небожителей. Том 3 — Мосян Тунсю",
            "Унесенные ветром — Маргарет Митчелл"
        ])
        self.layout.addWidget(self.book_list)

    def add_payment_selection(self):
        """Добавляет виджет выбора способа оплаты"""
        self.payment_label = QLabel("Выберите способ оплаты")
        self.payment_label.setStyleSheet("font-weight: bold; font-size: 14px; color: magenta;")
        self.layout.addWidget(self.payment_label)

        self.payment_group = QGroupBox()
        self.payment_layout = QVBoxLayout()
        self.payment_group.setLayout(self.payment_layout)

        self.payment_options = QButtonGroup()
        self.payment_radio_card = QRadioButton("По карте")
        self.payment_radio_qr = QRadioButton("По QR")
        self.payment_radio_cash = QRadioButton("Наличными")

        # Добавляем кнопки в группу и макет
        self.payment_options.addButton(self.payment_radio_card)
        self.payment_options.addButton(self.payment_radio_qr)
        self.payment_options.addButton(self.payment_radio_cash)

        self.payment_layout.addWidget(self.payment_radio_card)
        self.payment_layout.addWidget(self.payment_radio_qr)
        self.payment_layout.addWidget(self.payment_radio_cash)

        self.layout.addWidget(self.payment_group)

    def process_payment(self):
        """Обрабатывает нажатие кнопки 'Оплатить'"""
        selected_book = self.book_list.currentItem()
        selected_payment = None

        if self.payment_radio_card.isChecked():
            selected_payment = "По карте"
        elif self.payment_radio_qr.isChecked():
            selected_payment = "По QR"
        elif self.payment_radio_cash.isChecked():
            selected_payment = "Наличными"

        if selected_book and selected_payment:
            QMessageBox.information(
                self,
                "Оплата успешна",
                f"Вы выбрали книгу:\n{selected_book.text()}\n\nСпособ оплаты: {selected_payment}",
            )
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите книгу и способ оплаты!",
            )


# Основная точка входа в приложение
def main():
    app = QApplication(sys.argv)
    book_form = BookSelectionForm()
    book_form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
