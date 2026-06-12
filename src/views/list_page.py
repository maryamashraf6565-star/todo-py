from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QListWidgetItem)
from PyQt6.QtCore import pyqtSignal, Qt
from models.task import Task

class ListPage(QWidget):
    task_toggled = pyqtSignal(object)      # task, new_state (bool)
    add_task_requested = pyqtSignal()
    back_clicked = pyqtSignal()
    order_by_priority_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout(self)

        # --- Sidebar (left column) ---
        sidebar = QWidget()
        sidebar.setFixedWidth(150)
        sidebar_layout = QVBoxLayout(sidebar)

        self.add_task_btn = QPushButton("➕ Add Task")
        self.add_task_btn.clicked.connect(self.add_task_requested.emit)
        sidebar_layout.addWidget(self.add_task_btn)

        self.order_priority_btn = QPushButton("🔽 Order by Priority")
        self.order_priority_btn.clicked.connect(self.order_by_priority_requested.emit)
        sidebar_layout.addWidget(self.order_priority_btn)

        self.back_btn = QPushButton("⬅ Back to Lists")
        self.back_btn.clicked.connect(self.back_clicked.emit)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.back_btn)

        main_layout.addWidget(sidebar)

        # --- Main area (task list) ---
        right_area = QWidget()
        right_layout = QVBoxLayout(right_area)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        right_layout.addWidget(self.title_label)

        self.tasks_list = QListWidget()
        self.tasks_list.itemChanged.connect(self._on_item_changed)
        right_layout.addWidget(self.tasks_list)

        main_layout.addWidget(right_area, stretch=1)

    def set_list(self, todo_list):
        """Populate the task list with checkable items."""
        if todo_list is None:
            return

        self.title_label.setText(f"📋 {todo_list.name}  ({todo_list.get_task_count()} tasks)")

        self.tasks_list.clear()
        if todo_list.get_task_count() == 0:
            empty_item = QListWidgetItem("✨ List is empty — add a task!")
            empty_item.setFlags(Qt.ItemFlag.NoItemFlags)  # non-interactive
            self.tasks_list.addItem(empty_item)
            return

        for task in todo_list.tasks:
            # Create item text with priority indicator and deadline
            priority_symbol = {"red": "🔴", "orange": "🟠", "green": "🟢"}.get(task.get_priority_color(), "⚪")
            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
            display_text = f"{priority_symbol} {task.title}  [due: {deadline_str}]"

            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, task)  # store task object
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if task.completed else Qt.CheckState.Unchecked)

            # Set background color based on priority
            color = task.get_priority_color()
            if color == "red":
                bg = "#ffe6e6"
            elif color == "orange":
                bg = "#fff0e0"
            else:
                bg = "#e6ffe6"
            item.setBackground(Qt.GlobalColor.transparent)  # can't use hex directly? Use style sheet? Simpler:
            # We'll set via stylesheet on the list widget itself. But for item level, easier:
            # Actually QListWidgetItem.setBackground accepts QColor. We'll do:
            from PyQt6.QtGui import QColor
            item.setBackground(QColor(bg))

            self.tasks_list.addItem(item)

    def _on_item_changed(self, item):
        """When checkbox is toggled, emit signal with task object and new state."""
        if item.checkState() == Qt.CheckState.Checked:
            task = item.data(Qt.ItemDataRole.UserRole)
            if task and not task.completed:
                self.task_toggled.emit(task)