from PyQt6.QtWidgets import QApplication, QDialog, QStackedWidget , QMessageBox
from models.todo_list import TodoList
from models.task import Task
from views.main_windows import MainWindow
from views.list_page import ListPage
from views.add_task_dialog import AddTaskDialog
import json
from pathlib import Path

class AppController:
    def __init__(self):
        # Create QApplication only once
        self.app = QApplication([])
        self.stack = QStackedWidget()

        # Data - load from JSON or create defaults
        self.load_data()          # sets self.lists
        self.current_list = None

        # Views
        self.main_window = MainWindow()
        self.list_page = ListPage()

        # Connect signals
        self.main_window.list_selected.connect(self.show_list_page)
        self.main_window.new_list_requested.connect(self.add_new_list)
        self.main_window.delete_list_requested.connect(self.delete_list)
        
        self.list_page.add_task_requested.connect(self.show_add_task)
        self.list_page.back_clicked.connect(self.show_main)
        self.list_page.order_by_priority_requested.connect(self.order_current_list_by_priority)
        self.list_page.task_toggled.connect(self.on_task_completed)
        
        # Add pages to stack
        self.stack.addWidget(self.main_window)  # index 0
        self.stack.addWidget(self.list_page)    # index 1

        self.update_main_view()

    def update_main_view(self):
        self.main_window.update_lists(self.lists)

    def show_list_page(self, todo_list):
        if todo_list is None:
            return
        self.current_list = todo_list
        self.list_page.set_list(todo_list)
        self.stack.setCurrentWidget(self.list_page)

    def show_add_task(self):
        dialog = AddTaskDialog(self.stack)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_task_data()
            task = Task(
                title=data["title"],
                description=data["description"],
                deadline=data["deadline"],
                priority=data["priority"]
            )
            self.current_list.add_task(task)
            self.save_data()
            self.list_page.set_list(self.current_list)
            self.update_main_view()

    def show_main(self):
        self.update_main_view()
        self.stack.setCurrentWidget(self.main_window)

    def add_new_list(self, name: str):
        new_list = TodoList(name)
        self.lists.append(new_list)
        self.save_data()
        self.update_main_view()

    def order_current_list_by_priority(self):
        if self.current_list:
            self.current_list.tasks.sort(key=lambda t: t.priority, reverse=True)
            self.list_page.set_list(self.current_list)

    def on_task_completed(self, task):
        """Remove the task when checkbox is checked."""
        if self.current_list and task in self.current_list.tasks:
            self.current_list.remove_task(task)
            self.save_data()
            self.list_page.set_list(self.current_list)
            self.update_main_view()

    def run(self):
        self.stack.show()
        self.app.exec()

    def _get_data_file_path(self) -> Path:
        """Return path to JSON file in project root (same folder as src/)."""
        return Path(__file__).parent.parent.parent / "todo_data.json"

    def load_data(self):
        """Load lists from JSON file. If file missing, use default lists."""
        file_path = self._get_data_file_path()
        if not file_path.exists():
            self.lists = [
                TodoList("Work"),
                TodoList("Personal"),
                TodoList("Mariam")
            ]
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.lists = [TodoList.from_dict(list_data) for list_data in data.get("lists", [])]
            if not self.lists:
                self.lists = [TodoList("Work"), TodoList("Personal")]
        except Exception as e:
            print(f"Error loading data: {e}")
            self.lists = [TodoList("Work"), TodoList("Personal")]

    def delete_list(self, todo_list):
        #"""Delete a list after user confirmation."""
        # Ask for confirmation
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Delete",
            f"Are you sure you want to delete the list '{todo_list.name}'?\nAll tasks inside will be lost!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # Remove the list
        if todo_list in self.lists:
            self.lists.remove(todo_list)

        # If the deleted list was the currently open one, go back to main
        if self.current_list == todo_list:
            self.current_list = None
            self.stack.setCurrentWidget(self.main_window)

        # Save changes and refresh main view
        self.save_data()
        self.update_main_view()
    
    def save_data(self):
        """Save current lists to JSON file."""
        file_path = self._get_data_file_path()
        data = {
            "lists": [todo_list.to_dict() for todo_list in self.lists]
        }
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")