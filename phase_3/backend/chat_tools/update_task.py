"""
MCP tool for updating tasks via the AI chatbot.
Implements the update_task functionality as specified in the mcp-tools.md specification.
"""

import json
from typing import Dict, Any
from fastapi import HTTPException
from pydantic import BaseModel, Field
from datetime import date

from services.task_service import get_task_by_id, update_task
from models.task import TaskUpdate
from database import Session, engine
from .validation import validate_user_id


class UpdateTaskParams(BaseModel):
    """
    Parameters for the update_task tool based on mcp-tools.md specification.
    """
    task_id: int = Field(..., gt=0, description="ID of the task to update")
    title: str = Field(None, min_length=1, max_length=255, description="New title for the task (optional)")
    description: str = Field(None, max_length=1000, description="New description for the task (optional)")
    priority: str = Field(None, description="New priority level (optional)")
    due_date: str = Field(None, description="New due date in YYYY-MM-DD format (optional)")
    completed: bool = Field(None, description="Whether the task is completed (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1,
                "title": "Updated task title",
                "description": "Updated task description",
                "priority": "high",
                "due_date": "2023-12-31",
                "completed": True
            }
        }


def validate_task_id(task_id: int) -> bool:
    """
    Validate that task_id is a positive integer.

    Args:
        task_id: Task ID to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if task_id <= 0:
        raise ValueError("Task ID must be a positive integer")
    return True


def validate_priority(priority: str) -> bool:
    """
    Validate that priority is one of the allowed values.

    Args:
        priority: Priority value to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if not priority:
        return True

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


async def update_task_handler(user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for updating tasks based on mcp-tools.md specification.

    Args:
        user_id: ID of the authenticated user
        params: Parameters for the update_task operation

    Returns:
        Dict containing success status, task_id, updated_fields, and message
    """
    try:
        # Validate user_id
        validate_user_id(user_id)

        # Validate input parameters
        validated_params = UpdateTaskParams(**params)

        # Validate task_id
        validate_task_id(validated_params.task_id)

        # Validate priority if provided
        if validated_params.priority is not None:
            validate_priority(validated_params.priority)

        # Validate date format if provided
        if validated_params.due_date is not None:
            validate_date_format(validated_params.due_date)

        # Prepare update data, excluding unset fields
        update_data = {}
        if validated_params.title is not None:
            update_data["title"] = validated_params.title
        if validated_params.description is not None:
            update_data["description"] = validated_params.description
        if validated_params.priority is not None:
            update_data["priority"] = validated_params.priority
        if validated_params.due_date is not None:
            update_data["due_date"] = validated_params.due_date
        if validated_params.completed is not None:
            update_data["completed"] = validated_params.completed

        # Create database session and update task
        with Session(engine) as db_session:
            updated_task = update_task(
                db_session,
                validated_params.task_id,
                user_id,
                TaskUpdate(**update_data)
            )

            if not updated_task:
                return {
                    "success": False,
                    "error": f"Task with ID {validated_params.task_id} not found or you don't have permission to modify it"
                }

        # Determine which fields were updated
        updated_fields = list(update_data.keys())

        return {
            "success": True,
            "task_id": updated_task.id,
            "updated_fields": updated_fields,
            "message": f"Task '{updated_task.title}' updated successfully"
        }

    except ValueError as ve:
        return {
            "success": False,
            "error": f"Validation failed: {str(ve)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update task: {str(e)}"
        }