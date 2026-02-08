"""
Integration tests for the chat functionality.
Tests the integration between the API, agent, and MCP tools.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from main import app
from chat_api.chat import chat_endpoint, get_current_user
from chat_models.chat import ChatRequest, ChatMessage


def test_chat_endpoint_success(mock_auth):
    """Test the chat endpoint with successful interaction."""
    client = TestClient(app)
    user_id = mock_auth.id

    chat_request = {
        "messages": [
            {
                "role": "user",
                "content": "Add a task to buy groceries"
            }
        ]
    }

    with patch('chat_api.chat.chat_agent') as mock_chat_agent, \
         patch('database.Session') as mock_session_class:
        
        mock_chat_agent.process_conversation = AsyncMock(return_value="Mock response")
        
        # Configure mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None
        
        # We also need to mock conversation_service since it's used in the endpoint
        with patch('chat_api.chat.conversation_service') as mock_conv_service:
            mock_conv = MagicMock()
            mock_conv.id = "test-conv-id"
            mock_conv_service.create_conversation.return_value = mock_conv
            
            response = client.post(f"/api/v1/users/{user_id}/chat", json=chat_request)
            assert response.status_code == 200
            assert "conversation_id" in response.json()


@pytest.mark.asyncio
async def test_chat_endpoint_authentication():
    """Test the chat endpoint authentication requirements (direct call)."""
    user_id = "test-user-id"
    mock_current_user = MagicMock()
    mock_current_user.id = user_id

    chat_request = ChatRequest(
        messages=[
            ChatMessage(role="user", content="Add a task to buy groceries")
        ],
        user_id=user_id
    )

    with patch('chat_api.chat.chat_agent') as mock_chat_agent, \
         patch('database.Session') as mock_session_class:
        
        mock_chat_agent.process_conversation = AsyncMock(return_value="Task added successfully")
        
        # Configure mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        with patch('chat_api.chat.conversation_service') as mock_conv_service, \
             patch('chat_api.chat.message_service') as mock_msg_service:

            mock_conv = MagicMock()
            mock_conv.id = "test-conversation-id"
            mock_conv_service.create_conversation.return_value = mock_conv
            mock_msg_service.create_message.return_value = MagicMock()

            result = await chat_endpoint(user_id, chat_request, mock_current_user.id)
            assert hasattr(result, 'messages')
            mock_chat_agent.process_conversation.assert_called_once()


@pytest.mark.asyncio
async def test_chat_endpoint_unauthorized_access():
    """Test the chat endpoint when user_id doesn't match authenticated user."""
    user_id = "different-user-id"
    authenticated_user_id = "authenticated-user-id"
    mock_current_user = MagicMock()
    mock_current_user.id = authenticated_user_id

    chat_request = ChatRequest(
        messages=[
            ChatMessage(role="user", content="Add a task to buy groceries")
        ],
        user_id=user_id
    )

    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await chat_endpoint(user_id, chat_request, mock_current_user.id)

    assert exc_info.value.status_code == 403


def test_health_check_endpoint():
    """Test the health check endpoint."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready_check_endpoint():
    """Test the readiness check endpoint."""
    client = TestClient(app)
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


@pytest.mark.asyncio
async def test_conversation_history_endpoints():
    """Test the conversation history endpoints."""
    user_id = "test-user-id"
    mock_current_user = MagicMock()
    mock_current_user.id = user_id

    with patch('chat_api.chat.conversation_service') as mock_conv_service, \
         patch('database.Session') as mock_session_class:
        
        # Configure mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None
        
        mock_conversations = [MagicMock(), MagicMock()]
        mock_conv_service.get_user_conversations.return_value = mock_conversations

        from chat_api.chat import get_user_conversations
        result = await get_user_conversations(user_id, mock_current_user.id)
        assert result == mock_conversations


@pytest.mark.asyncio
async def test_specific_conversation_endpoint():
    """Test the specific conversation endpoint."""
    user_id = "test-user-id"
    conversation_id = "test-conversation-id"
    mock_current_user = MagicMock()
    mock_current_user.id = user_id

    with patch('chat_api.chat.conversation_service') as mock_conv_service, \
         patch('chat_api.chat.message_service') as mock_msg_service, \
         patch('database.Session') as mock_session_class:

        # Configure mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        mock_conversation = MagicMock()
        mock_messages = [MagicMock(), MagicMock()]
        mock_conv_service.get_conversation_by_id.return_value = mock_conversation
        mock_msg_service.get_messages_by_conversation.return_value = mock_messages

        from chat_api.chat import get_conversation
        result = await get_conversation(user_id, conversation_id, mock_current_user.id)
        assert result["conversation"] == mock_conversation
        assert result["messages"] == mock_messages