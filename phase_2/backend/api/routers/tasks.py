"""
Task endpoints for the Todo Web Application.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from database import get_session
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
from services.task_service import (
    get_task_by_id, get_tasks_by_user, create_task, update_task,
    delete_task, toggle_task_completion
)
from core.security import verify_token
from schemas.task import TaskResponse, TaskCreate as TaskCreateSchema, TaskUpdate as TaskUpdateSchema


router = APIRouter()


from fastapi import Header

def get_current_user_token(authorization: str = Header(default=None)) -> dict:
    """
    Extract and verify the current user's token from the Authorization header.

    Args:
        authorization: The Authorization header value

    Returns:
        dict: The verified token payload

    Raises:
        HTTPException: If the token is invalid or missing
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[len("Bearer "):]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: dict = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.

    Args:
        current_user: The currently authenticated user (extracted from token)
        session: Database session

    Returns:
        List[TaskResponse]: List of tasks owned by the user
    """
    user_id = current_user.get("sub")
    tasks = get_tasks_by_user(session, user_id)
    return tasks


@router.post("/", response_model=TaskResponse)
async def create_new_task(
    task_data: TaskCreateSchema,
    current_user: dict = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        current_user: The currently authenticated user (extracted from token)
        session: Database session

    Returns:
        TaskResponse: The created task

    Raises:
        HTTPException: If the user ID in the request doesn't match the authenticated user
    """
    user_id = current_user.get("sub")

    # Ensure the task is being created for the authenticated user
    if task_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create task for another user"
        )

    # Create the task
    task_create_obj = TaskCreate(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_id  # Use the user_id from the token instead of the request
    )

    db_task = create_task(session, task_create_obj)
    return db_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_single_task(
    task_id: int,
    current_user: dict = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to retrieve
        current_user: The currently authenticated user (extracted from token)
        session: Database session

    Returns:
        TaskResponse: The requested task

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    user_id = current_user.get("sub")
    db_task = get_task_by_id(session, task_id, user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )

    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    task_id: int,
    task_data: TaskUpdateSchema,
    current_user: dict = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Update a task if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to update
        task_data: Task update data
        current_user: The currently authenticated user (extracted from token)
        session: Database session

    Returns:
        TaskResponse: The updated task

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    user_id = current_user.get("sub")
    db_task = update_task(session, task_id, user_id, task_data)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )

    return db_task


@router.delete("/{task_id}")
async def delete_existing_task(
    task_id: int,
    current_user: dict = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Delete a task if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to delete
        current_user: The currently authenticated user (extracted from token)
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    user_id = current_user.get("sub")
    success = delete_task(session, task_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )

    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/toggle-complete", response_model=TaskResponse)
async def toggle_task_complete_status(
    task_id: int,
    current_user: dict = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task if it belongs to the authenticated user.

    Args:
        task_id: ID of the task to toggle
        current_user: The currently authenticated user (extracted from token)
        session: Database session

    Returns:
        TaskResponse: The updated task with toggled completion status

    Raises:
        HTTPException: If the task doesn't exist or doesn't belong to the user
    """
    user_id = current_user.get("sub")
    db_task = toggle_task_completion(session, task_id, user_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )

    return db_task