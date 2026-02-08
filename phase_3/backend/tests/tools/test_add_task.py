"""
Unit tests for the add_task MCP tool.
Tests the add_task functionality as specified in the mcp-tools.md specification.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import date

from chat_tools.add_task import add_task_handler, validate_priority, validate_date_format


@pytest.mark.asyncio
async def test_add_task_success():
    """Test successful addition of a task."""
    # Mock input parameters
    user_id = "test-user-id"
    params = {
        "title": "Test task",
        "description": "Test description",
        "priority": "medium",
        "due_date": "2023-12-31"
    }

    # Mock the database session and task creation
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test task"

    with patch('chat_tools.add_task.Session') as mock_session_class, \
         patch('chat_tools.add_task.engine') as mock_engine, \
         patch('chat_tools.add_task.create_task') as mock_create_task:

        # Configure the mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Configure the mock create_task function
        mock_create_task.return_value = mock_task

        # Call the handler
        result = await add_task_handler(user_id, params)

        # Assertions
        assert result["success"] is True
        assert result["task_id"] == 1
        assert "Task 'Test task' added successfully" in result["message"]

        # Verify that create_task was called
        mock_create_task.assert_called_once()


@pytest.mark.asyncio
async def test_add_task_missing_title():
    """Test adding a task with missing title (should fail validation)."""
    user_id = "test-user-id"
    params = {
        "description": "Test description",
        # Missing required title
    }

    result = await add_task_handler(user_id, params)

    assert result["success"] is False
    assert "Validation failed" in result["error"]


@pytest.mark.asyncio
async def test_add_task_invalid_priority():
    """Test adding a task with invalid priority."""
    user_id = "test-user-id"
    params = {
        "title": "Test task",
        "priority": "invalid_priority"
    }

    result = await add_task_handler(user_id, params)

    assert result["success"] is False
    assert "Validation failed" in result["error"]


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
