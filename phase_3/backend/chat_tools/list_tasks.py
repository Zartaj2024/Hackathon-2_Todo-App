"""
MCP tool for listing tasks via the AI chatbot.
Implements the list_tasks functionality as specified in the mcp-tools.md specification.
"""

import json
from typing import Dict, Any
from fastapi import HTTPException
from pydantic import BaseModel, Field

from services.task_service import get_tasks_by_user, get_task_by_id
from models.task import TaskRead
from database import Session, engine
from .validation import validate_user_id


class ListTasksParams(BaseModel):
    """
    Parameters for the list_tasks tool based on mcp-tools.md specification.
    """
    status: str = Field("all", description="Filter tasks by completion status (optional, defaults to all)")
    limit: int = Field(10, ge=1, le=100, description="Maximum number of tasks to return (optional, defaults to 10)")
    offset: int = Field(0, ge=0, description="Number of tasks to skip (for pagination, optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "all",
                "limit": 10,
                "offset": 0
            }
        }


def validate_status(status: str) -> bool:
    """
    Validate that status is one of the allowed values.

    Args:
        status: Status value to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    valid_statuses = ["all", "completed", "pending"]
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
    return True


def validate_limit(limit: int) -> bool:
    """
    Validate that limit is within the allowed range.

    Args:
        limit: Limit value to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")
    return True


def validate_offset(offset: int) -> bool:
    """
    Validate that offset is not negative.

    Args:
        offset: Offset value to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if offset < 0:
        raise ValueError("Offset must be greater than or equal to 0")
    return True


async def list_tasks_handler(user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for listing tasks based on mcp-tools.md specification.

    Args:
        user_id: ID of the authenticated user
        params: Parameters for the list_tasks operation

    Returns:
        Dict containing success status, tasks list, total count, and message
    """
    try:
        # Validate user_id
        validate_user_id(user_id)

        # Validate input parameters
        validated_params = ListTasksParams(**params)

        # Validate parameters
        validate_status(validated_params.status)
        validate_limit(validated_params.limit)
        validate_offset(validated_params.offset)

        # Create database session and get tasks
        with Session(engine) as db_session:
            all_tasks = get_tasks_by_user(db_session, user_id)

            # Apply status filter if needed
            filtered_tasks = all_tasks
            if validated_params.status == "completed":
                filtered_tasks = [task for task in all_tasks if task.completed]
            elif validated_params.status == "pending":
                filtered_tasks = [task for task in all_tasks if not task.completed]

            # Apply pagination
            start_idx = validated_params.offset
            end_idx = start_idx + validated_params.limit
            paginated_tasks = filtered_tasks[start_idx:end_idx]

            # Convert to dict format for response
            tasks_data = []
            for task in paginated_tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": str(task.due_date) if task.due_date else None,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                tasks_data.append(task_dict)

        return {
            "success": True,
            "tasks": tasks_data,
            "total_count": len(filtered_tasks),
            "message": f"Successfully retrieved {len(tasks_data)} task(s)"
        }

    except ValueError as ve:
        return {
            "success": False,
            "error": f"Validation failed: {str(ve)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list tasks: {str(e)}"
        }