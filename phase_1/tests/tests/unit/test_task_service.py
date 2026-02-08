"""
Unit tests for the TaskService class.

Tests all CRUD operations and validation for the task service.
"""

import pytest
from src.services.task_service import TaskService
from src.models.task import Task


def test_create_task_basic():
    """Test creating a task with title only."""
    service = TaskService(skip_auth=True)
    task = service.create_task("Test task")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == ""
    assert task.completed is False


def test_create_task_with_description():
    """Test creating a task with title and description."""
    service = TaskService(skip_auth=True)
    task = service.create_task("Test task", "Test description")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed is False


def test_create_multiple_tasks_unique_ids():
    """Test that multiple tasks get unique IDs."""
    service = TaskService(skip_auth=True)
    task1 = service.create_task("First task")
    task2 = service.create_task("Second task")
    task3 = service.create_task("Third task")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3


def test_get_all_tasks_empty():
    """Test getting all tasks when none exist."""
    service = TaskService(skip_auth=True)
    tasks = service.get_all_tasks()

    assert len(tasks) == 0


def test_get_all_tasks_with_items():
    """Test getting all tasks when some exist."""
    service = TaskService(skip_auth=True)
    service.create_task("First task")
    service.create_task("Second task")
    service.create_task("Third task")

    tasks = service.get_all_tasks()

    assert len(tasks) == 3
    assert tasks[0].title == "First task"
    assert tasks[1].title == "Second task"
    assert tasks[2].title == "Third task"


def test_get_task_by_id_exists():
    """Test getting a specific task by ID."""
    service = TaskService(skip_auth=True)
    created_task = service.create_task("Test task")

    retrieved_task = service.get_task_by_id(created_task.id)

    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == created_task.title


def test_get_task_by_id_not_exists():
    """Test getting a task by ID that doesn't exist."""
    service = TaskService(skip_auth=True)
    service.create_task("Existing task")

    retrieved_task = service.get_task_by_id(999)

    assert retrieved_task is None


def test_update_task_title():
    """Test updating a task's title."""
    service = TaskService(skip_auth=True)
    original_task = service.create_task("Original title")

    updated_task = service.update_task(original_task.id, "New title")

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == "New title"
    assert updated_task.description == original_task.description


def test_update_task_description():
    """Test updating a task's description."""
    service = TaskService(skip_auth=True)
    original_task = service.create_task("Title", "Original description")

    # We need to recreate the task with the new description
    updated_task = service.update_task(original_task.id, None, "New description")

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == original_task.title
    assert updated_task.description == "New description"


def test_update_task_both_fields():
    """Test updating both title and description."""
    service = TaskService(skip_auth=True)
    original_task = service.create_task("Original title", "Original description")

    updated_task = service.update_task(original_task.id, "New title", "New description")

    assert updated_task is not None
    assert updated_task.id == original_task.id
    assert updated_task.title == "New title"
    assert updated_task.description == "New description"


def test_update_task_invalid_id():
    """Test updating a task with an invalid ID."""
    service = TaskService(skip_auth=True)
    service.create_task("Existing task")

    result = service.update_task(999, "New title")

    assert result is None


def test_update_task_empty_title_validation():
    """Test that updating with an empty title raises ValueError."""
    service = TaskService(skip_auth=True)
    original_task = service.create_task("Original title")

    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        service.update_task(original_task.id, "")


def test_delete_task_exists():
    """Test deleting a task that exists."""
    service = TaskService(skip_auth=True)
    task_to_delete = service.create_task("Task to delete")

    result = service.delete_task(task_to_delete.id)

    assert result is True
    # Verify the task is gone
    assert service.get_task_by_id(task_to_delete.id) is None


def test_delete_task_not_exists():
    """Test deleting a task that doesn't exist."""
    service = TaskService(skip_auth=True)
    service.create_task("Existing task")

    result = service.delete_task(999)

    assert result is False


def test_toggle_completion():
    """Test toggling a task's completion status."""
    service = TaskService(skip_auth=True)
    task = service.create_task("Test task")

    # Initially should be False
    assert task.completed is False

    # Toggle it
    toggled_task = service.toggle_completion(task.id)

    assert toggled_task is not None
    assert toggled_task.completed is True

    # Toggle it again
    toggled_again_task = service.toggle_completion(task.id)

    assert toggled_again_task is not None
    assert toggled_again_task.completed is False


def test_toggle_completion_not_exists():
    """Test toggling completion for a task that doesn't exist."""
    service = TaskService(skip_auth=True)
    service.create_task("Existing task")

    result = service.toggle_completion(999)

    assert result is None


def test_task_auto_generation_of_ids():
    """Test that IDs are auto-generated and sequential."""
    service = TaskService(skip_auth=True)

    task1 = service.create_task("First")
    task2 = service.create_task("Second")
    task3 = service.create_task("Third")

    # Delete the second task
    service.delete_task(task2.id)

    # Create a new task - it should get ID 4, not reuse ID 2
    task4 = service.create_task("Fourth")

    assert task1.id == 1
    assert task2.id == 2  # This was deleted
    assert task3.id == 3
    assert task4.id == 4  # Should be 4, not reuse 2


def test_get_all_tasks_sorted_by_id():
    """Test that get_all_tasks returns tasks sorted by ID."""
    service = TaskService(skip_auth=True)
    task1 = service.create_task("First")   # This will have ID 1
    task2 = service.create_task("Second")  # This will have ID 2
    task3 = service.create_task("Third")   # This will have ID 3

    tasks = service.get_all_tasks()

    # Should be sorted by ID: 1, 2, 3
    assert tasks[0].id == 1
    assert tasks[1].id == 2
    assert tasks[2].id == 3
    assert tasks[0].title == "First"
    assert tasks[1].title == "Second"
    assert tasks[2].title == "Third"