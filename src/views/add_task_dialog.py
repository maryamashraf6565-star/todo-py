from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                             QTextEdit, QPushButton, QFormLayout,
                             QComboBox, QDateEdit)
from PyQt6.QtCore import QDate
from datetime import datetime
from models.task import Task

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task")
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        self.title_input = QLineEdit()
        layout.addRow("Title:", self.title_input)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        layout.addRow("Description:", self.desc_input)

        # Priority dropdown
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low (green)", "Medium (yellow)", "High (red)"])
        layout.addRow("Priority:", self.priority_combo)

        # Deadline date picker
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDate(QDate.currentDate().addDays(7))
        layout.addRow("Deadline:", self.deadline_edit)

        self.add_btn = QPushButton("Add Task")
        self.add_btn.clicked.connect(self.accept)
        layout.addRow(self.add_btn)

    def get_task_data(self):
        """Return a dict suitable for creating a Task object."""
        priority_map = {0: Task.PRIORITY_LOW, 1: Task.PRIORITY_MEDIUM, 2: Task.PRIORITY_HIGH}
        deadline_qdate = self.deadline_edit.date()
        deadline = datetime(deadline_qdate.year(), deadline_qdate.month(), deadline_qdate.day())
        return {
            "title": self.title_input.text(),
            "description": self.desc_input.toPlainText(),
            "deadline": deadline,
            "priority": priority_map[self.priority_combo.currentIndex()]
        }