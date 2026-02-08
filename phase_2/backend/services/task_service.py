"""
Business logic for task operations in the Todo Web Application.
"""

from sqlmodel import Session, select
from typing import Optional

from models.user import User
from models.task import Task, TaskCreate, TaskUpdate


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.

    Args:
        session: Database session
        email: Email address to search for

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """
    Get a user by their ID.

    Args:
        session: Database session
        user_id: User ID to search for

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()


def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a task by its ID for a specific user.

    Args:
        session: Database session
        task_id: Task ID to search for
        user_id: User ID that should own the task

    Returns:
        Optional[Task]: Task object if found and owned by user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return session.exec(statement).first()


def get_tasks_by_user(session: Session, user_id: str) -> list[Task]:
    """
    Get all tasks for a specific user.

    Args:
        session: Database session
        user_id: User ID to get tasks for

    Returns:
        list[Task]: List of tasks owned by the user
    """
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()


def create_task(session: Session, task_data: TaskCreate) -> Task:
    """
    Create a new task.

    Args:
        session: Database session
        task_data: Task creation data

    Returns:
        Task: Created task object
    """
    db_task = Task.from_orm(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def update_task(session: Session, task_id: int, user_id: str, task_data: TaskUpdate) -> Optional[Task]:
    """
    Update an existing task.

    Args:
        session: Database session
        task_id: Task ID to update
        user_id: User ID that should own the task
        task_data: Task update data

    Returns:
        Optional[Task]: Updated task object if successful, None if not found or not owned by user
    """
    db_task = get_task_by_id(session, task_id, user_id)
    if not db_task:
        return None

    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a task.

    Args:
        session: Database session
        task_id: Task ID to delete
        user_id: User ID that should own the task

    Returns:
        bool: True if deletion was successful, False if task not found or not owned by user
    """
    db_task = get_task_by_id(session, task_id, user_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Toggle the completion status of a task.

    Args:
        session: Database session
        task_id: Task ID to toggle
        user_id: User ID that should own the task

    Returns:
        Optional[Task]: Updated task object if successful, None if not found or not owned by user
    """
    db_task = get_task_by_id(session, task_id, user_id)
    if not db_task:
        return None

    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task