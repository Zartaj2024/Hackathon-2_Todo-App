"""
Unit tests for the update_task MCP tool.
Tests the update_task functionality as specified in the mcp-tools.md specification.
"""

import pytest
from unittest.mock import patch, MagicMock

from chat_tools.update_task import update_task_handler, validate_task_id, validate_priority, validate_date_format


@pytest.mark.asyncio
async def test_update_task_success():
    """Test successful update of a task."""
    # Mock input parameters
    user_id = "test-user-id"
    params = {
        "task_id": 1,
        "title": "Updated Task Title",
        "description": "Updated Description",
        "priority": "high",
        "due_date": "2023-12-31",
        "completed": True
    }

    # Mock the updated task
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Updated Task Title"
    mock_task.description = "Updated Description"
    mock_task.priority = "high"
    mock_task.due_date = "2023-12-31"
    mock_task.completed = True

    with patch('chat_tools.update_task.Session') as mock_session_class, \
         patch('chat_tools.update_task.engine') as mock_engine, \
         patch('chat_tools.update_task.update_task') as mock_update_task:

        # Configure the mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Configure the mock update_task function
        mock_update_task.return_value = mock_task

        # Call the handler
        result = await update_task_handler(user_id, params)

        # Assertions
        assert result["success"] is True
        assert result["task_id"] == 1
        assert "updated successfully" in result["message"]
        assert "title" in result["updated_fields"] or "description" in result["updated_fields"]

        # Verify that update_task was called
        mock_update_task.assert_called_once()


@pytest.mark.asyncio
async def test_update_task_partial_updates():
    """Test updating only specific fields of a task."""
    user_id = "test-user-id"
    params = {
        "task_id": 1,
        "title": "Updated Title",
        # Only updating title
    }

    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Updated Title"
    mock_task.description = "Original Description"
    mock_task.completed = False

    with patch('chat_tools.update_task.Session') as mock_session_class, \
         patch('chat_tools.update_task.engine') as mock_engine, \
         patch('chat_tools.update_task.update_task') as mock_update_task:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        mock_update_task.return_value = mock_task

        result = await update_task_handler(user_id, params)

        assert result["success"] is True
        assert result["task_id"] == 1
        # Only title should be in updated_fields
        assert "title" in result["updated_fields"]
        assert len(result["updated_fields"]) >= 1


@pytest.mark.asyncio
async def test_update_task_not_found():
    """Test updating a task that doesn't exist."""
    user_id = "test-user-id"
    params = {
        "task_id": 999,  # Non-existent task
        "title": "New Title"
    }

    with patch('chat_tools.update_task.Session') as mock_session_class, \
         patch('chat_tools.update_task.engine') as mock_engine, \
         patch('chat_tools.update_task.update_task') as mock_update_task:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Configure the mock update_task function to return None (task not found)
        mock_update_task.return_value = None

        result = await update_task_handler(user_id, params)

        assert result["success"] is False
        assert "not found or you don't have permission" in result["error"]


@pytest.mark.asyncio
async def test_update_task_invalid_task_id():
    """Test updating a task with invalid task ID."""
    user_id = "test-user-id"
    params = {
        "task_id": -1,  # Invalid task ID
        "title": "New Title"
    }

    result = await update_task_handler(user_id, params)

    assert result["success"] is False
    assert "Validation failed" in result["error"]


def test_validate_task_id_valid():
    """Test task ID validation with valid values."""
    valid_task_ids = [1, 10, 100, 999999]

    for task_id in valid_task_ids:
        assert validate_task_id(task_id) is True


def test_validate_task_id_invalid():
    """Test task ID validation with invalid values."""
    invalid_task_ids = [0, -1, -10]

    for task_id in invalid_task_ids:
        with pytest.raises(ValueError):
            validate_task_id(task_id)


def test_validate_priority_valid():
    """Test priority validation with valid values."""
    valid_priorities = ["low", "medium", "high"]

    for priority in valid_priorities:
        assert validate_priority(priority) is True


def test_validate_priority_invalid():
    """Test priority validation with invalid values."""
    invalid_priority = "super_high"

    with pytest.raises(ValueError):
        validate_priority(invalid_priority)


def test_validate_date_format_valid():
    """Test date format validation with valid dates."""
    valid_dates = ["2023-12-31", "2024-01-01", "2023-02-28"]

    for date_str in valid_dates:
        assert validate_date_format(date_str) is True


def test_validate_date_format_invalid():
    """Test date format validation with invalid dates."""
    invalid_dates = ["2023-13-01", "2023-12-32", "invalid-date", "2023/12/31"]

    for date_str in invalid_dates:
        with pytest.raises(ValueError):
            validate_date_format(date_str)


def test_validate_date_format_none():
    """Test date format validation with None (should be valid)."""
    assert validate_date_format(None) is True
