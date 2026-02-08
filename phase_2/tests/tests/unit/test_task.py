"""
Unit tests for the Task model.

Tests all functionality of the Task class including:
- Initialization with all attributes
- Title validation
- String representations
- Dictionary conversion
"""

import pytest
from src.models.task import Task


def test_task_initialization_with_required_fields():
    """Test creating a Task with only required fields."""
    task = Task(1, "Buy groceries")

    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == ""
    assert task.completed is False


def test_task_initialization_with_all_fields():
    """Test creating a Task with all fields provided."""
    task = Task(2, "Complete project", "Finish the todo app project", True)

    assert task.id == 2
    assert task.title == "Complete project"
    assert task.description == "Finish the todo app project"
    assert task.completed is True


def test_task_title_validation_empty():
    """Test that creating a Task with an empty title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        Task(1, "")


def test_task_title_validation_whitespace_only():
    """Test that creating a Task with whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        Task(1, "   ")


def test_task_title_stripped():
    """Test that title is stripped of leading/trailing whitespace."""
    task = Task(1, "  Clean the house  ")

    assert task.title == "Clean the house"


def test_task_str_representation():
    """Test the string representation of a task."""
    task = Task(1, "Sample task")
    expected = "[○] 1. Sample task"

    assert str(task) == expected


def test_task_str_completed():
    """Test the string representation of a completed task."""
    task = Task(1, "Completed task", completed=True)
    expected = "[✓] 1. Completed task"

    assert str(task) == expected


def test_task_str_with_description():
    """Test the string representation of a task with description."""
    task = Task(1, "Task with desc", "This is a description")
    expected = "[○] 1. Task with desc\n   This is a description"

    assert str(task) == expected


def test_task_repr():
    """Test the developer representation of a task."""
    task = Task(1, "Sample task")
    expected = "Task(id=1, title='Sample task', description='', completed=False)"

    assert repr(task) == expected


def test_task_to_dict():
    """Test converting a task to dictionary."""
    task = Task(1, "Sample task", "A description", True)
    expected = {
        "id": 1,
        "title": "Sample task",
        "description": "A description",
        "completed": True
    }

    assert task.to_dict() == expected


def test_task_from_dict():
    """Test creating a task from dictionary."""
    data = {
        "id": 2,
        "title": "From dict task",
        "description": "Created from dict",
        "completed": True
    }
    task = Task.from_dict(data)

    assert task.id == 2
    assert task.title == "From dict task"
    assert task.description == "Created from dict"
    assert task.completed is True


def test_task_from_dict_optional_fields():
    """Test creating a task from dictionary with missing optional fields."""
    data = {
        "id": 3,
        "title": "Minimal task"
    }
    task = Task.from_dict(data)

    assert task.id == 3
    assert task.title == "Minimal task"
    assert task.description == ""
    assert task.completed is False