"""
MCP tool for completing tasks via the AI chatbot.
Implements the complete_task functionality as specified in the mcp-tools.md specification.
"""

import json
from typing import Dict, Any
from fastapi import HTTPException
from pydantic import BaseModel, Field

from services.task_service import get_task_by_id, toggle_task_completion
from models.task import TaskRead
from database import Session, engine
from .validation import validate_user_id


class CompleteTaskParams(BaseModel):
    """
    Parameters for the complete_task tool based on mcp-tools.md specification.
    """
    task_id: int = Field(..., gt=0, description="ID of the task to mark as completed")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": 1
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


async def complete_task_handler(user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for completing tasks based on mcp-tools.md specification.

    Args:
        user_id: ID of the authenticated user
        params: Parameters for the complete_task operation

    Returns:
        Dict containing success status, task_id, and message
    """
    try:
        # Validate user_id
        validate_user_id(user_id)

        # Validate input parameters
        validated_params = CompleteTaskParams(**params)

        # Validate task_id
        validate_task_id(validated_params.task_id)

        # Create database session and complete task
        with Session(engine) as db_session:
            updated_task = toggle_task_completion(db_session, validated_params.task_id, user_id)

            if not updated_task:
                return {
                    "success": False,
                    "error": f"Task with ID {validated_params.task_id} not found or you don't have permission to modify it"
                }

        return {
            "success": True,
            "task_id": updated_task.id,
            "message": f"Task '{updated_task.title}' marked as completed"
        }

    except ValueError as ve:
        return {
            "success": False,
            "error": f"Validation failed: {str(ve)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to complete task: {str(e)}"
        }