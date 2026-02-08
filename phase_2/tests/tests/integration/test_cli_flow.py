"""
Integration tests for the CLI flow.

Tests the end-to-end functionality of the CLI interface with the task service.
"""

import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
from src.services.task_service import TaskService
from src.cli.cli_interface import CLIInterface


def test_add_task_integration():
    """Test adding a task through CLI interface."""
    service = TaskService()
    cli = CLIInterface(service)

    # Mock user input for title and description
    with patch('builtins.input', side_effect=['New Task', 'This is a description']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.add_task()

    # Verify task was added
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "New Task"
    assert tasks[0].description == "This is a description"
    assert tasks[0].completed is False


def test_add_task_without_description():
    """Test adding a task without description."""
    service = TaskService()
    cli = CLIInterface(service)

    # Mock user input for title and empty description
    with patch('builtins.input', side_effect=['New Task', '']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.add_task()

    # Verify task was added with empty description
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "New Task"
    assert tasks[0].description == ""
    assert tasks[0].completed is False


def test_view_all_tasks_empty():
    """Test viewing all tasks when none exist."""
    service = TaskService()
    cli = CLIInterface(service)

    with patch('sys.stdout', new_callable=StringIO) as fake_out:
        cli.view_all_tasks()

    output = fake_out.getvalue()
    assert "No tasks found." in output


def test_view_all_tasks_with_items():
    """Test viewing all tasks when some exist."""
    service = TaskService()
    cli = CLIInterface(service)

    # Add some tasks directly
    service.create_task("First Task", "Description 1")
    service.create_task("Second Task", "Description 2")

    with patch('sys.stdout', new_callable=StringIO) as fake_out:
        cli.view_all_tasks()

    output = fake_out.getvalue()
    assert "First Task" in output
    assert "Second Task" in output
    assert "Description 1" in output
    assert "Description 2" in output


def test_update_task():
    """Test updating a task through CLI interface."""
    service = TaskService()
    cli = CLIInterface(service)

    # Add a task first
    original_task = service.create_task("Original Title", "Original Description")

    # Mock user input for task ID, new title, and new description
    with patch('builtins.input', side_effect=[str(original_task.id), 'Updated Title', 'Updated Description']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.update_task()

    # Verify task was updated
    updated_task = service.get_task_by_id(original_task.id)
    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"


def test_update_task_keep_current_values():
    """Test updating a task but keeping current values."""
    service = TaskService()
    cli = CLIInterface(service)

    # Add a task first
    original_task = service.create_task("Original Title", "Original Description")

    # Mock user input for task ID, empty title (to keep current), empty description (to keep current)
    with patch('builtins.input', side_effect=[str(original_task.id), '', '']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.update_task()

    # Verify task still has original values
    unchanged_task = service.get_task_by_id(original_task.id)
    assert unchanged_task is not None
    assert unchanged_task.title == "Original Title"
    assert unchanged_task.description == "Original Description"


def test_delete_task():
    """Test deleting a task through CLI interface."""
    service = TaskService()
    cli = CLIInterface(service)

    # Add a task first
    task_to_delete = service.create_task("Task to Delete")

    # Mock user input for task ID
    with patch('builtins.input', side_effect=[str(task_to_delete.id)]):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.delete_task()

    # Verify task was deleted
    deleted_task = service.get_task_by_id(task_to_delete.id)
    assert deleted_task is None

    # Verify there are no tasks left
    tasks = service.get_all_tasks()
    assert len(tasks) == 0


def test_toggle_completion():
    """Test toggling task completion through CLI interface."""
    service = TaskService()
    cli = CLIInterface(service)

    # Add a task first
    task = service.create_task("Task to Toggle")

    # Mock user input for task ID
    with patch('builtins.input', side_effect=[str(task.id)]):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.toggle_completion()

    # Verify task completion was toggled
    toggled_task = service.get_task_by_id(task.id)
    assert toggled_task is not None
    assert toggled_task.completed is True


def test_toggle_completion_back():
    """Test toggling task completion twice (back to original state)."""
    service = TaskService()
    cli = CLIInterface(service)

    # Add a task first
    task = service.create_task("Task to Toggle")

    # First toggle - should complete it
    with patch('builtins.input', side_effect=[str(task.id)]):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.toggle_completion()

    # Verify task completion was toggled to True
    task_after_first_toggle = service.get_task_by_id(task.id)
    assert task_after_first_toggle is not None
    assert task_after_first_toggle.completed is True

    # Second toggle - should make it incomplete again
    with patch('builtins.input', side_effect=[str(task.id)]):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.toggle_completion()

    # Verify task completion was toggled back to False
    task_after_second_toggle = service.get_task_by_id(task.id)
    assert task_after_second_toggle is not None
    assert task_after_second_toggle.completed is False


def test_invalid_task_id_operations():
    """Test operations with invalid task IDs."""
    service = TaskService()
    cli = CLIInterface(service)

    # Test updating with invalid ID
    with patch('builtins.input', side_effect=['999', 'New Title', 'New Description']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.update_task()
    output = fake_out.getvalue()
    assert "No task found with ID 999" in output

    # Test deleting with invalid ID
    output = ""  # Reset
    with patch('builtins.input', side_effect=['999']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.delete_task()
    output = fake_out.getvalue()
    assert "No task found with ID 999" in output

    # Test toggling with invalid ID
    output = ""  # Reset
    with patch('builtins.input', side_effect=['999']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.toggle_completion()
    output = fake_out.getvalue()
    assert "No task found with ID 999" in output


def test_invalid_input_handling():
    """Test handling of invalid input (non-numeric IDs)."""
    service = TaskService()
    cli = CLIInterface(service)

    # Test updating with non-numeric ID
    with patch('builtins.input', side_effect=['invalid', 'New Title', 'New Description']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.update_task()
    output = fake_out.getvalue()
    assert "Invalid task ID" in output

    # Test deleting with non-numeric ID
    output = ""  # Reset
    with patch('builtins.input', side_effect=['invalid']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.delete_task()
    output = fake_out.getvalue()
    assert "Invalid task ID" in output

    # Test toggling with non-numeric ID
    output = ""  # Reset
    with patch('builtins.input', side_effect=['invalid']):
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            cli.toggle_completion()
    output = fake_out.getvalue()
    assert "Invalid task ID" in output