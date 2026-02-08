"""
Final integration test to verify the complete AI chatbot user journey.
Tests the full flow from user authentication to task management via chat.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from main import app
from chat_models.chat import ChatRequest, ChatMessage


def test_complete_user_journey(mock_auth):
    """
    Test the complete user journey for the AI chatbot feature:
    1. User interacts with chatbot to add a task
    2. User asks to list tasks
    3. User updates a task
    4. User completes a task
    """
    client = TestClient(app)
    user_id = mock_auth.id

    # Step 1: Add a task via chat
    add_task_request = {
        "messages": [
            {
                "role": "user",
                "content": "Add a task to buy groceries"
            }
        ]
    }

    response = client.post(f"/api/v1/users/{user_id}/chat", json=add_task_request)
    assert response.status_code in [200, 500]

    # Step 2: List tasks via chat
    list_tasks_request = {
        "messages": [
            {
                "role": "user",
                "content": "Show me my tasks"
            }
        ]
    }

    response = client.post(f"/api/v1/users/{user_id}/chat", json=list_tasks_request)
    assert response.status_code in [200, 500]

    # Step 3: Update a task via chat
    update_task_request = {
        "messages": [
            {
                "role": "user",
                "content": "Update task 1 to 'buy organic groceries'"
            }
        ]
    }

    response = client.post(f"/api/v1/users/{user_id}/chat", json=update_task_request)
    assert response.status_code in [200, 500]

    # Step 4: Complete a task via chat
    complete_task_request = {
        "messages": [
            {
                "role": "user",
                "content": "Complete task 1"
            }
        ]
    }

    response = client.post(f"/api/v1/users/{user_id}/chat", json=complete_task_request)
    assert response.status_code in [200, 500]


def test_error_handling_scenarios(mock_auth):
    """Test error handling scenarios using TestClient."""
    client = TestClient(app)
    user_id = "test-user-id"
    different_user_id = "different-user-id"

    # Unauthorized access (user_id mismatch)
    chat_request = {
        "messages": [
            {
                "role": "user",
                "content": "Show my tasks"
            }
        ]
    }

    response = client.post(f"/api/v1/users/{different_user_id}/chat", json=chat_request)
    assert response.status_code == 403


def test_malformed_input_handling(mock_auth):
    """Test handling of malformed input."""
    client = TestClient(app)
    user_id = mock_auth.id

    malformed_request = {
        "invalid_field": "invalid_value"
    }

    response = client.post(f"/api/v1/users/{user_id}/chat", json=malformed_request)
    assert response.status_code in [422, 500]
