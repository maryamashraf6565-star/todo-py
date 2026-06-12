from typing import List
from .task import Task

class TodoList:
    def __init__(self, name: str, tasks: List[Task] = None):
        self.name = name
        self.tasks = tasks or []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)

    def get_task_count(self) -> int:
        return len(self.tasks)

    def get_tasks_sorted_by_priority(self) -> List[Task]:
        return sorted(self.tasks, key=lambda t: t.priority, reverse=True)

    def to_dict(self) -> dict:
        """Convert TodoList to dict."""
        return {
            "name": self.name,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoList":
        """Recreate TodoList from dict."""
        tasks = [Task.from_dict(task_data) for task_data in data["tasks"]]
        return cls(name=data["name"], tasks=tasks)