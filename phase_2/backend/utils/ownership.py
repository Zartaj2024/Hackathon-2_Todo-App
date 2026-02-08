"""
Task ownership validation utilities for the Todo Web Application.
"""

from sqlmodel import Session, select
from typing import Optional

from ..models.task import Task


def verify_task_ownership(session: Session, task_id: int, user_id: str) -> bool:
    """
    Verify that a task belongs to the specified user.

    Args:
        session: Database session
        task_id: ID of the task to verify ownership for
        user_id: ID of the user claiming ownership

    Returns:
        bool: True if the user owns the task, False otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task is not None


def get_task_owner(session: Session, task_id: int) -> Optional[str]:
    """
    Get the owner of a task.

    Args:
        session: Database session
        task_id: ID of the task to get owner for

    Returns:
        Optional[str]: User ID of the task owner if found, None otherwise
    """
    statement = select(Task.user_id).where(Task.id == task_id)
    result = session.exec(statement).first()
    return result


def user_can_access_task(session: Session, task_id: int, user_id: str) -> bool:
    """
    Check if a user can access a specific task.

    Args:
        session: Database session
        task_id: ID of the task to check access for
        user_id: ID of the user requesting access

    Returns:
        bool: True if the user can access the task, False otherwise
    """
    return verify_task_ownership(session, task_id, user_id)