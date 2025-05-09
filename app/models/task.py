from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from ..db import db
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")
    completed_at: Mapped[Optional[datetime]]

    def to_dict(self):
        """Return object attributes in dictionary format.

        When called on a Task object, the method returns a dictionary
        containing key value pairs corresponding to the object's attributes.
        """
        task = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at),
        }
        if self.goal_id:  # adds "goal_id" field if goal_id exists
            task["goal_id"] = self.goal_id

        return task


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
