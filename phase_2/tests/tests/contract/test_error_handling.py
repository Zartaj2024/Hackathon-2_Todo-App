"""
Contract tests for error handling requirements.

Tests that all error handling requirements are properly implemented.
"""

import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.cli.cli_interface import CLIInterface


def test_empty_title_validation():
    """Test that empty titles are rejected with validation errors (FR-008)."""
    service = TaskService()

    # Test creating a task with empty title
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        service.create_task("")

    # Test creating a task with whitespace-only title
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        service.create_task("   ")

    # Test updating a task with empty title
    task = service.create_task("Valid task")
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        service.update_task(task.id, "")


def test_invalid_task_id_handling():
    """Test that invalid task IDs are handled gracefully with clear error messages (FR-009)."""
    service = TaskService()

    # Add a task first
    existing_task = service.create_task("Existing task")

    # Test getting a non-existent task
    result = service.get_task_by_id(999)
    assert result is None

    # Test updating a non-existent task
    result = service.update_task(999, "New title")
    assert result is None

    # Test deleting a non-existent task
    result = service.delete_task(999)
    assert result is False

    # Test toggling completion for a non-existent task
    result = service.toggle_completion(999)
    assert result is None


def test_all_user_inputs_are_validated():
    """Test that all user inputs are validated to prevent application crashes (FR-010)."""
    service = TaskService()

    # Test that invalid ID types are handled gracefully
    # This should not crash the application
    result = service.get_task_by_id("invalid")
    assert result is None

    # Test that very long titles are rejected
    long_title = "t" * 1001  # More than 1000 characters
    with pytest.raises(ValueError, match="Task title cannot exceed 1000 characters"):
        service.create_task(long_title)

    # Test that very long descriptions are rejected
    service = TaskService()  # Reset to avoid title validation
    long_desc = "d" * 5001  # More than 5000 characters
    with pytest.raises(ValueError, match="Task description cannot exceed 5000 characters"):
        Task(1, "Valid title", long_desc)


def test_clear_error_messages_for_validation_failures():
    """Test that clear error messages are provided for all validation failures (FR-011)."""
    service = TaskService()

    # Test empty title error message
    with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
        service.create_task("")

    # Test long title error message
    with pytest.raises(ValueError, match="Task title cannot exceed 1000 characters"):
        service.create_task("t" * 1001)

    # Test long description error message
    with pytest.raises(ValueError, match="Task description cannot exceed 5000 characters"):
        Task(1, "Valid title", "d" * 5001)


def test_application_never_crashes_due_to_user_input_errors():
    """Test that the application never crashes due to user input errors (FR-012)."""
    service = TaskService()

    # Test various invalid inputs that should not crash the application
    try:
        # Invalid ID types
        service.get_task_by_id(None)
        service.get_task_by_id([])
        service.get_task_by_id({})
        service.get_task_by_id(-1)
        service.get_task_by_id(3.14)

        # Invalid titles
        service.create_task("")
        service.create_task("   ")
        service.create_task(123)  # Non-string type

        # Valid task for further testing
        task = service.create_task("Test task")

        # Invalid updates
        service.update_task(task.id, "")
        service.update_task(-1, "Valid title")
        service.update_task("invalid", "Valid title")

        # Invalid deletes
        service.delete_task(-1)
        service.delete_task("invalid")

        # Invalid toggles
        service.toggle_completion(-1)
        service.toggle_completion("invalid")

    except Exception as e:
        # If any of these operations cause a crash (any exception not related to validation),
        # then the requirement is not met
        if not isinstance(e, ValueError):
            pytest.fail(f"Application crashed with unexpected error: {e}")


def test_application_returns_to_usable_state_after_errors():
    """Test that the application returns to a usable state after any error occurs (FR-013)."""
    service = TaskService()

    # Add a valid task first
    original_task = service.create_task("Original task")

    # Cause various errors
    error_occurred = False
    try:
        service.create_task("")  # Should raise ValueError
    except ValueError:
        error_occurred = True

    assert error_occurred, "Expected a ValueError to occur"

    # Verify the service is still functional
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Original task"

    # Try another operation that should work
    new_task = service.create_task("New task after error")
    assert new_task is not None
    assert new_task.title == "New task after error"

    # Verify both tasks exist
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 2


def test_extremely_long_text_inputs_handled():
    """Test that extremely long text inputs are handled appropriately (edge case)."""
    service = TaskService()

    # Test maximum allowed title length
    max_title = "t" * 1000
    task = service.create_task(max_title)
    assert task.title == max_title

    # Test maximum allowed description length
    service2 = TaskService()  # New service to avoid title conflict
    max_desc = "d" * 5000
    task2 = service2.create_task("Valid title", max_desc)
    assert task2.description == max_desc

    # Test exceeding maximum lengths should raise errors
    with pytest.raises(ValueError):
        service.create_task("t" * 1001)  # Too long title

    with pytest.raises(ValueError):
        Task(1, "Valid title", "d" * 5001)  # Too long description


def test_whitespace_only_inputs_handled():
    """Test that whitespace-only inputs are handled as validation errors."""
    service = TaskService()

    # Test various whitespace-only inputs
    whitespace_inputs = [" ", "   ", "\t", "\n", "\r\n", "\t\n\r "]

    for ws_input in whitespace_inputs:
        with pytest.raises(ValueError, match="Task title cannot be empty or contain only whitespace"):
            service.create_task(ws_input)


def test_non_numeric_inputs_handled_gracefully():
    """Test that non-numeric inputs where numbers are expected are handled gracefully."""
    service = TaskService()

    # These should not crash the application
    result = service.get_task_by_id("abc")
    assert result is None

    result = service.get_task_by_id([1, 2, 3])
    assert result is None

    result = service.get_task_by_id({"id": 1})
    assert result is None

    result = service.get_task_by_id(None)
    assert result is None


def test_safe_error_messages_no_internal_details():
    """Test that error messages don't leak internal details."""
    service = TaskService()

    # Create a task
    task = service.create_task("Test task")

    # Try to update with invalid data
    try:
        service.update_task("invalid_id", 123)
    except Exception as e:
        # The error message should be user-friendly and not expose internal details
        error_msg = str(e)
        # Check that it's a proper validation error message
        assert "Invalid" in error_msg or "failed" in error_msg.lower()


def test_error_recovery_mechanisms():
    """Test that error recovery mechanisms return to usable state."""
    service = TaskService()

    # Perform operations that might cause errors
    initial_count = len(service.get_all_tasks())

    # Cause an error
    try:
        service.create_task("")
    except ValueError:
        pass  # Expected

    # Verify state is still consistent
    after_error_count = len(service.get_all_tasks())
    assert after_error_count == initial_count

    # Verify we can still add a valid task
    valid_task = service.create_task("Valid task after error")
    assert valid_task is not None

    final_count = len(service.get_all_tasks())
    assert final_count == initial_count + 1