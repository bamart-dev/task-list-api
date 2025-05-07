from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]

    def to_dict(self):
        """Return object attributes in dictionary format.

        When called on a Task object, the method returns a dictionary
        containing key value pairs corresponding to the object's attributes.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at),
        }


    @classmethod
    def create_from_dict(cls, task_data):
        """Create new task from dictionary items.

        Instantiates and returns a new Task object with attribute values
        derived from a provided dictionary.
        """
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data.get("completed_at"),
        )
