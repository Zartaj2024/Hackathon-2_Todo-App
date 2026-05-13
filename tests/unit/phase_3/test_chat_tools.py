import pytest
from unittest.mock import MagicMock, patch
from chat_tools.add_task import add_task_handler
from chat_tools.list_tasks import list_tasks_handler

@pytest.mark.asyncio
async def test_add_task_tool():
    # Mocking the creation of a task
    mock_task = MagicMock()
    mock_task.id = 123
    mock_task.title = "AI Task"

    with patch("chat_tools.add_task.create_task", return_value=mock_task):
        with patch("chat_tools.add_task.validate_user_id", return_value=True):
            result = await add_task_handler(
                user_id="test-user",
                params={
                    "title": "AI Task",
                    "description": "From tool"
                }
            )

            assert result["success"] is True
            assert result["task_id"] == 123
            assert "Task 'AI Task' added successfully" in result["message"]

@pytest.mark.asyncio
async def test_list_tasks_tool():
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Task 1"
    mock_task.completed = False
    mock_task.priority = "medium"
    mock_task.due_date = None

    with patch("chat_tools.list_tasks.get_tasks_by_user", return_value=[mock_task]):
        with patch("chat_tools.list_tasks.validate_user_id", return_value=True):
            result = await list_tasks_handler(user_id="test-user", params={})
            assert result["success"] is True
            assert result["total_count"] == 1
            assert result["tasks"][0]["title"] == "Task 1"
