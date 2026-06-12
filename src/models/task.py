from datetime import datetime
from typing import Optional

class Task:
    PRIORITY_HIGH = 3
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 1

    def __init__(self, title: str, description: str = "", 
                 deadline: Optional[datetime] = None,
                 priority: int = PRIORITY_MEDIUM,
                 created_at: Optional[datetime] = None,
                 completed: bool = False):
        self.title = title
        self.description = description
        self.created_at = created_at or datetime.now()
        self.deadline = deadline
        self.priority = priority
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def get_priority_color(self) -> str:
        if self.priority == self.PRIORITY_HIGH:
            return "red"
        elif self.priority == self.PRIORITY_MEDIUM:
            return "orange"
        else:
            return "green"

    def to_dict(self) -> dict:
        """Convert Task to JSON-serializable dict."""
        return {
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "priority": self.priority,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Recreate a Task from a dict (loaded from JSON)."""
        created_at = datetime.fromisoformat(data["created_at"]) if data["created_at"] else None
        deadline = datetime.fromisoformat(data["deadline"]) if data["deadline"] else None
        return cls(
            title=data["title"],
            description=data["description"],
            created_at=created_at,
            deadline=deadline,
            priority=data["priority"],
            completed=data["completed"]
        )