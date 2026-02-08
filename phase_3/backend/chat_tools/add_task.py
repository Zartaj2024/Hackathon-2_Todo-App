"""
MCP tool for adding tasks via the AI chatbot.
Implements the add_task functionality as specified in the mcp-tools.md specification.
"""

import json
from typing import Dict, Any
from fastapi import HTTPException
from pydantic import BaseModel, Field
from datetime import date

from services.task_service import create_task
from models.task import TaskCreate
from database import Session, engine
from .validation import validate_user_id


class AddTaskParams(BaseModel):
    """
    Parameters for the add_task tool based on mcp-tools.md specification.
    """
    title: str = Field(..., min_length=1, max_length=255, description="Title of the task to be created")
    description: str = Field(None, max_length=1000, description="Detailed description of the task (optional)")
    priority: str = Field("medium", description="Priority level of the task (optional, defaults to medium)")
    due_date: str = Field(None, description="Due date in YYYY-MM-DD format (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "medium",
                "due_date": "2023-12-31"
            }
        }


def validate_priority(priority: str) -> bool:
    """
    Validate that priority is one of the allowed values.

    Args:
        priority: Priority value to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    valid_priorities = ["low", "medium", "high"]
    if priority not in valid_priorities:
        raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
    return True


def validate_date_format(date_str: str) -> bool:
    """
    Validate that date string is in YYYY-MM-DD format.

    Args:
        date_str: Date string to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if not date_str:
        return True

    import re
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        raise ValueError("Date must be in YYYY-MM-DD format")

    # Additional validation to check if it's a real date
    try:
        date.fromisoformat(date_str)
    except ValueError:
        raise ValueError("Invalid date")

    return True


async def add_task_handler(user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for adding tasks based on mcp-tools.md specification.

    Args:
        user_id: ID of the authenticated user
        params: Parameters for the add_task operation

    Returns:
        Dict containing success status, task_id, and message
    """
    try:
        # Validate user_id
        validate_user_id(user_id)

        # Validate input parameters
        validated_params = AddTaskParams(**params)

        # Validate priority
        validate_priority(validated_params.priority)

        # Validate date format if provided
        if validated_params.due_date:
            validate_date_format(validated_params.due_date)

        # Prepare task data
        task_data = TaskCreate(
            title=validated_params.title,
            description=validated_params.description,
            completed=False,
            user_id=user_id,
            priority=validated_params.priority,
            due_date=validated_params.due_date,
            ai_processed=True  # Mark as created via AI
        )

        # Create database session and add task
        with Session(engine) as db_session:
            created_task = create_task(db_session, task_data)

        return {
            "success": True,
            "task_id": created_task.id,
            "message": f"Task '{created_task.title}' added successfully"
        }

    except ValueError as ve:
        return {
            "success": False,
            "error": f"Validation failed: {str(ve)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to add task: {str(e)}"
        }