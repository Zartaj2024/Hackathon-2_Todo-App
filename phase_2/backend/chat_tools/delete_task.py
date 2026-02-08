"""
MCP tool for deleting tasks via the AI chatbot.
Implements the delete_task functionality as specified in the mcp-tools.md specification.
"""

import json
from typing import Dict, Any
from fastapi import HTTPException
from pydantic import BaseModel, Field

from services.task_service import get_task_by_id, delete_task
from models.task import TaskRead
from database import Session, engine
from .validation import validate_user_id


class DeleteTaskParams(BaseModel):
    """
    Parameters for the delete_task tool based on mcp-tools.md specification.
    """
    task_id: int = Field(..., gt=0, description="ID of the task to delete")

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


async def delete_task_handler(user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for deleting tasks based on mcp-tools.md specification.

    Args:
        user_id: ID of the authenticated user
        params: Parameters for the delete_task operation

    Returns:
        Dict containing success status, task_id, and message
    """
    try:
        # Validate user_id
        validate_user_id(user_id)

        # Validate input parameters
        validated_params = DeleteTaskParams(**params)

        # Validate task_id
        validate_task_id(validated_params.task_id)

        # Create database session and delete task
        with Session(engine) as db_session:
            success = delete_task(db_session, validated_params.task_id, user_id)

            if not success:
                return {
                    "success": False,
                    "error": f"Task with ID {validated_params.task_id} not found or you don't have permission to delete it"
                }

        return {
            "success": True,
            "task_id": validated_params.task_id,
            "message": f"Task with ID {validated_params.task_id} deleted successfully"
        }

    except ValueError as ve:
        return {
            "success": False,
            "error": f"Validation failed: {str(ve)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete task: {str(e)}"
        }