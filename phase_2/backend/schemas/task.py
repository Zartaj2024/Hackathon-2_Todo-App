"""
Task schemas for the Todo Web Application.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    """
    Base schema for task with shared attributes.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    user_id: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and fruits",
                "completed": False,
                "user_id": "user-id-string"
            }
        }


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """
    Schema for returning task data.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskOwnershipCheck(BaseModel):
    """
    Schema for checking task ownership.
    """
    task_id: int
    user_id: str