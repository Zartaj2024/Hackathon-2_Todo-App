"""
Task model for the Todo Web Application.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User  # Use relative import to avoid circular imports
    from .conversation import Conversation  # Needed for relationship validation


class TaskBase(SQLModel):
    """
    Base class for Task model containing shared attributes.
    """
    title: str = Field(nullable=False, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task entity representing a task owned by a user.

    Attributes:
        id: Unique identifier for the task
        title: Task title (required, max 255 characters)
        description: Optional task description (nullable, max 1000 characters)
        completed: Whether the task is completed (default: false)
        user_id: Reference to the owning user
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        ai_processed: Whether this task was created via AI (default: false)
    """
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)  # Added index for performance
    ai_processed: bool = Field(default=False)  # Added for AI integration

    # Relationship to User
    user: "User" = Relationship(back_populates="tasks")

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def __str__(self):
        return f"Task(id={self.id}, title={self.title}, completed={self.completed}, user_id={self.user_id})"

    def __repr__(self):
        return self.__str__()

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Sample task",
                "description": "Sample task description",
                "completed": False,
                "user_id": "user-uuid-string",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }


class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: int
    user_id: str
    ai_processed: bool
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    user_id: str = Field(..., min_length=1, max_length=255)
    ai_processed: bool = Field(default=False)

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and fruits",
                "completed": False,
                "user_id": "user-id-string",
                "ai_processed": False
            }
        }


class TaskUpdate(SQLModel):
    """
    Schema for updating task information.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    ai_processed: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated task title",
                "description": "Updated task description",
                "completed": True,
                "ai_processed": True
            }
        }


