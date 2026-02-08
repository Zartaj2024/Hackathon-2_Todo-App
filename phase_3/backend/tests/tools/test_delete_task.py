"""
Unit tests for the delete_task MCP tool.
Tests the delete_task functionality as specified in the mcp-tools.md specification.
"""

import pytest
from unittest.mock import patch, MagicMock

from chat_tools.delete_task import delete_task_handler, validate_task_id


@pytest.mark.asyncio
async def test_delete_task_success():
    """Test successful deletion of a task."""
    # Mock input parameters
    user_id = "test-user-id"
    params = {
        "task_id": 1
    }

    with patch('chat_tools.delete_task.Session') as mock_session_class, \
         patch('chat_tools.delete_task.engine') as mock_engine, \
         patch('chat_tools.delete_task.delete_task') as mock_delete_task:

        # Configure the mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Configure the mock delete_task function to return True (success)
        mock_delete_task.return_value = True

        # Call the handler
        result = await delete_task_handler(user_id, params)

        # Assertions
        assert result["success"] is True
        assert result["task_id"] == 1
        assert "deleted successfully" in result["message"]

        # Verify that delete_task was called
        mock_delete_task.assert_called_once_with(mock_session_instance, 1, user_id)


@pytest.mark.asyncio
async def test_delete_task_not_found():
    """Test deleting a task that doesn't exist."""
    user_id = "test-user-id"
    params = {
        "task_id": 999  # Non-existent task
    }

    with patch('chat_tools.delete_task.Session') as mock_session_class, \
         patch('chat_tools.delete_task.engine') as mock_engine, \
         patch('chat_tools.delete_task.delete_task') as mock_delete_task:

        # Configure the mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Configure the mock delete_task function to return False (task not found)
        mock_delete_task.return_value = False

        # Call the handler
        result = await delete_task_handler(user_id, params)

        # Assertions
        assert result["success"] is False
        assert "not found or you don't have permission" in result["error"]

        # Verify that delete_task was called
        mock_delete_task.assert_called_once_with(mock_session_instance, 999, user_id)


@pytest.mark.asyncio
async def test_delete_task_invalid_task_id():
    """Test deleting a task with invalid task ID."""
    user_id = "test-user-id"
    params = {
        "task_id": -1  # Invalid task ID
    }

    result = await delete_task_handler(user_id, params)

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
