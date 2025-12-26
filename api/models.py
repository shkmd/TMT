from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Task:
    def __init__(self, id: str, title: str, description: str = "",
                 status: TaskStatus = TaskStatus.TODO,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 assigned_to: Optional[str] = None,
                 due_date: Optional[datetime] = None,
                 tags: Optional[list] = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.assigned_to = assigned_to
        self.due_date = due_date
        self.tags = tags or []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "assigned_to": self.assigned_to,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
