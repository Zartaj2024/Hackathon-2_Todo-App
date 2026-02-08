"""
Unit tests for the complete_task MCP tool.
Tests the complete_task functionality as specified in the mcp-tools.md specification.
"""

import pytest
from unittest.mock import patch, MagicMock

from chat_tools.complete_task import complete_task_handler, validate_task_id


@pytest.mark.asyncio
async def test_complete_task_success():
    """Test successful completion of a task."""
    # Mock input parameters
    user_id = "test-user-id"
    params = {
        "task_id": 1
    }

    # Mock the updated task
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.completed = True

    with patch('chat_tools.complete_task.Session') as mock_session_class, \
         patch('chat_tools.complete_task.engine') as mock_engine, \
         patch('chat_tools.complete_task.toggle_task_completion') as mock_toggle_task:

        # Configure the mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Configure the mock toggle_task_completion function
        mock_toggle_task.return_value = mock_task

        # Call the handler
        result = await complete_task_handler(user_id, params)

        # Assertions
        assert result["success"] is True
        assert result["task_id"] == 1
        assert "marked as completed" in result["message"]

        # Verify that toggle_task_completion was called
        mock_toggle_task.assert_called_once_with(mock_session_instance, 1, user_id)


@pytest.mark.asyncio
async def test_complete_task_not_found():
    """Test completing a task that doesn't exist."""
    user_id = "test-user-id"
    params = {
        "task_id": 999  # Non-existent task
    }

    with patch('chat_tools.complete_task.Session') as mock_session_class, \
         patch('chat_tools.complete_task.engine') as mock_engine, \
         patch('chat_tools.complete_task.toggle_task_completion') as mock_toggle_task:

        # Configure the mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Configure the mock toggle_task_completion function to return None (task not found)
        mock_toggle_task.return_value = None

        # Call the handler
        result = await complete_task_handler(user_id, params)

        # Assertions
        assert result["success"] is False
        assert "not found or you don't have permission" in result["error"]

        # Verify that toggle_task_completion was called
        mock_toggle_task.assert_called_once_with(mock_session_instance, 999, user_id)


@pytest.mark.asyncio
async def test_complete_task_invalid_task_id():
    """Test completing a task with invalid task ID."""
    user_id = "test-user-id"
    params = {
        "task_id": -1  # Invalid task ID
    }

    result = await complete_task_handler(user_id, params)

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
