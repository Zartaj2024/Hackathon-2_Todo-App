import pytest
from unittest.mock import MagicMock, patch
from chat_tools.complete_task import complete_task_handler
from chat_tools.update_task import update_task_handler
from chat_tools.delete_task import delete_task_handler

@pytest.mark.asyncio
async def test_complete_task_tool():
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.completed = True

    with patch("chat_tools.complete_task.toggle_task_completion", return_value=mock_task):
        with patch("chat_tools.complete_task.validate_user_id", return_value=True):
            result = await complete_task_handler(user_id="test-user", params={"task_id": 1})
            assert result["success"] is True
            assert "completed" in result["message"]

@pytest.mark.asyncio
async def test_update_task_tool():
    mock_task = MagicMock()
    mock_task.title = "Updated Title"

    with patch("chat_tools.update_task.update_task", return_value=mock_task):
        with patch("chat_tools.update_task.validate_user_id", return_value=True):
            result = await update_task_handler(
                user_id="test-user",
                params={"task_id": 1, "title": "Updated Title"}
            )
            assert result["success"] is True
            assert "Updated Title" in result["message"]

@pytest.mark.asyncio
async def test_delete_task_tool():
    with patch("chat_tools.delete_task.delete_task", return_value=True):
        with patch("chat_tools.delete_task.validate_user_id", return_value=True):
            result = await delete_task_handler(user_id="test-user", params={"task_id": 1})
            assert result["success"] is True
            assert "deleted" in result["message"]
