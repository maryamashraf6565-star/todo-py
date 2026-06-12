from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QListWidget, QInputDialog)
from PyQt6.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    list_selected = pyqtSignal(object)      # emits TodoList on double-click
    new_list_requested = pyqtSignal(str)    # emits new list name
    delete_list_requested = pyqtSignal(object)  # emits TodoList to delete

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo Lists")
        self.setGeometry(250, 250, 600, 500)

        self.todo_lists = []

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Your Lists:"))

        self.lists_widget = QListWidget()
        layout.addWidget(self.lists_widget)

        self.add_list_btn = QPushButton("➕ New List")
        self.add_list_btn.clicked.connect(self._on_add_list_clicked)
        layout.addWidget(self.add_list_btn)

        self.delete_list_btn = QPushButton("❌ Delete Selected List")
        self.delete_list_btn.clicked.connect(self._on_delete_list_clicked)
        layout.addWidget(self.delete_list_btn)

        # Only double-click opens the list; single click just selects
        self.lists_widget.itemDoubleClicked.connect(self._on_list_double_clicked)

    def update_lists(self, todo_lists):
        self.todo_lists = todo_lists
        self.lists_widget.clear()
        for lst in todo_lists:
            self.lists_widget.addItem(f"{lst.name} ({lst.get_task_count()} tasks)")

    def _on_list_double_clicked(self, item):
        list_name = item.text().split(" (")[0]
        selected = next((lst for lst in self.todo_lists if lst.name == list_name), None)
        if selected:
            self.list_selected.emit(selected)

    def _on_add_list_clicked(self):
        name, ok = QInputDialog.getText(self, "New List", "Enter list name:")
        if ok and name.strip():
            self.new_list_requested.emit(name.strip())

    def _on_delete_list_clicked(self):
        current_item = self.lists_widget.currentItem()
        if not current_item:
            # No list selected
            return
        list_name = current_item.text().split(" (")[0]
        selected_list = next((lst for lst in self.todo_lists if lst.name == list_name), None)
        if selected_list:
            self.delete_list_requested.emit(selected_list)