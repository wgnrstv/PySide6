import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout, QMessageBox, QDialog, QLabel, QLineEdit,
    QTextEdit, QDateTimeEdit
)
from PySide6.QtCore import Qt, QTimer, QDateTime
from datetime import datetime

NOTES_FILE = 'notes.json'

class Note:
    def __init__(self, title, content, created_at=None, deadline=None):
        self.title = title
        self.content = content
        self.created_at = created_at or datetime.now().isoformat()
        self.deadline = deadline

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'deadline': self.deadline
        }

    @staticmethod
    def from_dict(data):
        return Note(
            title=data['title'],
            content=data['content'],
            created_at=data.get('created_at'),
            deadline=data.get('deadline')
        )

class NotesManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.notes = [Note.from_dict(note) for note in data]
        else:
            self.notes = []

    def save_notes(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([note.to_dict() for note in self.notes], f, ensure_ascii=False, indent=4)

    def add_note(self, note):
        self.notes.append(note)
        self.save_notes()

    def update_note(self, index, new_note):
        if 0 <= index < len(self.notes):
            self.notes[index] = new_note
            self.save_notes()

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            self.save_notes()

class NoteDialog(QDialog):
    def __init__(self, parent=None, note=None):
        super().__init__(parent)
        self.setWindowTitle("Заметка")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Заголовок")
        layout.addWidget(QLabel("Заголовок:"))
        layout.addWidget(self.title_edit)

        self.content_edit = QTextEdit()
        layout.addWidget(QLabel("Содержание:"))
        layout.addWidget(self.content_edit)

        self.deadline_edit = QDateTimeEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(QLabel("Дедлайн:"))
        layout.addWidget(self.deadline_edit)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        if note:
            self.title_edit.setText(note.title)
            self.content_edit.setText(note.content)
            if note.deadline:
                self.deadline_edit.setDateTime(QDateTime.fromString(note.deadline, Qt.ISODate))

    def get_note_data(self):
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
        deadline = self.deadline_edit.dateTime().toString(Qt.ISODate)
        return title, content, deadline

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер Заметок")
        self.resize(600, 400)

        self.manager = NotesManager(NOTES_FILE)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)

        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        main_layout.addLayout(buttons_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.add_button.clicked.connect(self.add_note)
        self.edit_button.clicked.connect(self.edit_note)
        self.delete_button.clicked.connect(self.delete_note)

        self.load_notes_into_list()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_deadlines)
        self.timer.start(60000)

    def load_notes_into_list(self):
        self.list_widget.clear()
        for note in self.manager.notes:
            item_text = f"{note.title} - Создано: {self.format_datetime(note.created_at)}"
            if note.deadline:
                remaining = self.get_time_remaining(note.deadline)
                item_text += f" - Дедлайн: {self.format_datetime(note.deadline)} ({remaining})"
            self.list_widget.addItem(item_text)

    def format_datetime(self, dt_str):
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%Y-%m-%d %H:%M")

    def get_time_remaining(self, deadline_str):
        deadline = datetime.fromisoformat(deadline_str)
        now = datetime.now()
        delta = deadline - now
        if delta.total_seconds() > 0:
            days, seconds = delta.days, delta.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{days}д {hours}ч {minutes}м"
        else:
            return "Просрочено"

    def add_note(self):
        dialog = NoteDialog(self)
        if dialog.exec() == QDialog.Accepted:
            title, content, deadline = dialog.get_note_data()
            if title:
                new_note = Note(title=title, content=content, deadline=deadline)
                self.manager.add_note(new_note)
                self.load_notes_into_list()
            else:
                QMessageBox.warning(self, "Ошибка", "Заголовок не может быть пустым.")

    def edit_note(self):
        selected = self.list_widget.currentRow()
        if selected >= 0:
            note = self.manager.notes[selected]
            dialog = NoteDialog(self, note)
            if dialog.exec() == QDialog.Accepted:
                title, content, deadline = dialog.get_note_data()
                if title:
                    updated_note = Note(title=title, content=content, created_at=note.created_at, deadline=deadline)
                    self.manager.update_note(selected, updated_note)
                    self.load_notes_into_list()
                else:
                    QMessageBox.warning(self, "Ошибка", "Заголовок не может быть пустым.")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку для редактирования.")

    def delete_note(self):
        selected = self.list_widget.currentRow()
        if selected >= 0:
            reply = QMessageBox.question(
                self, 'Подтверждение',
                'Вы уверены, что хотите удалить выбранную заметку?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.manager.delete_note(selected)
                self.load_notes_into_list()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку для удаления.")

    def update_deadlines(self):
        self.load_notes_into_list()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
