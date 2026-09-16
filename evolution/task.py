from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Task:

    title: str
    description: str
    task_type: str

    priority: int = 5

    status: str = "pending"

    attempts: int = 0

    created: str = field(
        default_factory=lambda:
        datetime.now().isoformat()
    )

    id: str = field(
        default_factory=lambda:
        str(uuid.uuid4())
    )

    metadata: dict = field(default_factory=dict)

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "task_type": self.task_type,
            "priority": self.priority,
            "status": self.status,
            "attempts": self.attempts,
            "created": self.created,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data):

        task = cls(
            title=data["title"],
            description=data["description"],
            task_type=data["task_type"]
        )

        task.id = data["id"]
        task.priority = data["priority"]
        task.status = data["status"]
        task.attempts = data["attempts"]
        task.created = data["created"]
        task.metadata = data["metadata"]

        return task