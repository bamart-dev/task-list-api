from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")


    def to_dict(self):
        """Return object attributes in dictionary format.

        Returns a dictionary containing key value pairs corresponding
        to the Goal object's attributes.
        """
        return {
            "id": self.id,
            "title": self.title,
        }


    @classmethod
    def create_from_dict(cls, goal_data):
        """Create new goal from dictionary.

        Instantiates and returns a new Goal object with attributes
        derived from the provided dictionary.
        """
        return cls(
            title = goal_data["title"],
        )
