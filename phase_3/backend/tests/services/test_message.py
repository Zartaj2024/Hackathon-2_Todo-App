"""
Unit tests for the message service.
Tests the message service functionality for CRUD operations.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from uuid import uuid4

from chat_services.message_service import MessageService
from models.message import MessageCreate


def test_create_message():
    """Test creating a new message."""
    # Create a mock message service
    service = MessageService()

    # Mock data
    conversation_id = str(uuid4())
    message_data = MessageCreate(
        conversation_id=conversation_id,
        role="user",
        content="Test message content",
        message_type="text"  # Required field
    )

    # Create a mock conversation object to validate existence
    mock_conversation = MagicMock()

    with patch('chat_services.message_service.Session') as mock_session_class, \
         patch('chat_services.message_service.select') as mock_select, \
         patch('chat_services.message_service.Conversation') as mock_conversation_model:

        # Configure the mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the conversation query execution to return a conversation
        mock_conversation_exec_result = MagicMock()
        mock_conversation_exec_result.first.return_value = mock_conversation
        mock_session_instance.exec.return_value = mock_conversation_exec_result

        # Mock the add, commit, and refresh methods
        mock_session_instance.add = MagicMock()
        mock_session_instance.commit = MagicMock()
        mock_session_instance.refresh = MagicMock()

        # Call the method
        result = service.create_message(mock_session_instance, message_data)

        # Assertions
        mock_session_instance.add.assert_called_once()
        added_msg = mock_session_instance.add.call_args[0][0]
        assert added_msg.conversation_id == conversation_id
        assert added_msg.role == "user"
        assert added_msg.content == "Test message content"
        assert added_msg.message_type == "text"
        
        mock_session_instance.commit.assert_called_once()
        mock_session_instance.refresh.assert_called_once_with(added_msg)


def test_create_message_conversation_not_found():
    """Test creating a message when conversation doesn't exist."""
    service = MessageService()

    conversation_id = str(uuid4())
    message_data = MessageCreate(
        conversation_id=conversation_id,
        role="user",
        content="Test message content"
    )

    with patch('chat_services.message_service.Session') as mock_session_class, \
         patch('chat_services.message_service.select') as mock_select:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the conversation query execution to return None
        mock_conversation_exec_result = MagicMock()
        mock_conversation_exec_result.first.return_value = None
        mock_session_instance.exec.return_value = mock_conversation_exec_result

        # Expect an HTTPException to be raised
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            service.create_message(mock_session_instance, message_data)

        assert exc_info.value.status_code == 404
        assert "Conversation not found" in exc_info.value.detail


def test_get_messages_by_conversation():
    """Test getting all messages for a conversation."""
    service = MessageService()

    conversation_id = str(uuid4())
    user_id = "test-user-id"

    # Create mock messages
    mock_msg1 = MagicMock()
    mock_msg1.id = str(uuid4())
    mock_msg1.conversation_id = conversation_id
    mock_msg1.role = "user"
    mock_msg1.content = "Message 1"

    mock_msg2 = MagicMock()
    mock_msg2.id = str(uuid4())
    mock_msg2.conversation_id = conversation_id
    mock_msg2.role = "assistant"
    mock_msg2.content = "Message 2"

    mock_messages = [mock_msg1, mock_msg2]

    # Create mock conversation to validate ownership
    mock_conversation = MagicMock()
    mock_conversation.id = conversation_id
    mock_conversation.user_id = user_id

    with patch('chat_services.message_service.Session') as mock_session_class, \
         patch('chat_services.message_service.select') as mock_select, \
         patch('chat_services.message_service.Conversation') as mock_conversation_model:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the conversation query execution
        mock_conversation_exec_result = MagicMock()
        mock_conversation_exec_result.first.return_value = mock_conversation
        mock_session_instance.exec.return_value = mock_conversation_exec_result

        # Mock the message query execution
        mock_message_exec_result = MagicMock()
        mock_message_exec_result.all.return_value = mock_messages
        mock_session_instance.exec.return_value = mock_message_exec_result

        # Mock the MessageRead model validation
        with patch('chat_services.message_service.MessageRead.model_validate') as mock_model_validate:
            mock_model_validate.side_effect = lambda x: MagicMock()  # Return mock for each conversion

            # Call the method
            result = service.get_messages_by_conversation(mock_session_instance, conversation_id, user_id)

            # Assertions
            mock_select.assert_called()
            mock_message_exec_result.all.assert_called_once()
            assert mock_model_validate.call_count == len(mock_messages)


def test_get_messages_by_conversation_unauthorized():
    """Test getting messages when user doesn't own the conversation."""
    service = MessageService()

    conversation_id = str(uuid4())
    user_id = "test-user-id"

    with patch('chat_services.message_service.Session') as mock_session_class, \
         patch('chat_services.message_service.select') as mock_select:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the conversation query execution to return None (not owned by user)
        mock_conversation_exec_result = MagicMock()
        mock_conversation_exec_result.first.return_value = None
        mock_session_instance.exec.return_value = mock_conversation_exec_result

        # Expect an HTTPException to be raised
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            service.get_messages_by_conversation(mock_session_instance, conversation_id, user_id)

        assert exc_info.value.status_code == 404
        assert "Conversation not found or you don't have permission" in exc_info.value.detail


def test_update_message():
    """Test updating a message."""
    service = MessageService()

    message_id = str(uuid4())
    user_id = "test-user-id"
    conversation_id = str(uuid4())

    # Create mock message and conversation objects
    mock_message = MagicMock()
    mock_message.id = message_id
    mock_message.conversation_id = conversation_id
    mock_message.content = "Old content"

    mock_conversation = MagicMock()
    mock_conversation.id = conversation_id
    mock_conversation.user_id = user_id

    mock_update_data = MagicMock()
    mock_update_data.model_dump.return_value = {"content": "New content"}

    with patch('chat_services.message_service.Session') as mock_session_class, \
         patch('chat_services.message_service.select') as mock_select:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the message query execution
        mock_message_exec_result = MagicMock()
        mock_message_exec_result.first.return_value = mock_message
        mock_session_instance.exec.return_value = mock_message_exec_result

        # Mock the conversation query execution (for ownership check)
        mock_conversation_exec_result = MagicMock()
        mock_conversation_exec_result.first.return_value = mock_conversation
        # Need to set up exec to return different results based on query
        mock_session_instance.exec.side_effect = [mock_message_exec_result, mock_conversation_exec_result]

        # Mock the MessageRead model validation
        with patch('chat_services.message_service.MessageRead.model_validate') as mock_model_validate:
            mock_model_validate.return_value = MagicMock()

            # Mock the MessageUpdate object
            mock_message_update = MagicMock()
            mock_message_update.model_dump.return_value = {"content": "New content"}

            # Call the method
            result = service.update_message(mock_session_instance, message_id, user_id, mock_message_update)

            # Assertions
            assert mock_message.content == "New content"
            mock_session_instance.add.assert_called_once_with(mock_message)
            mock_session_instance.commit.assert_called_once()
            mock_session_instance.refresh.assert_called_once_with(mock_message)


def test_delete_message():
    """Test deleting a message."""
    service = MessageService()

    message_id = str(uuid4())
    user_id = "test-user-id"
    conversation_id = str(uuid4())

    # Create mock message and conversation objects
    mock_message = MagicMock()
    mock_message.id = message_id
    mock_message.conversation_id = conversation_id

    mock_conversation = MagicMock()
    mock_conversation.id = conversation_id
    mock_conversation.user_id = user_id

    with patch('chat_services.message_service.Session') as mock_session_class, \
         patch('chat_services.message_service.select') as mock_select:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the message query execution
        mock_message_exec_result = MagicMock()
        mock_message_exec_result.first.return_value = mock_message
        mock_session_instance.exec.return_value = mock_message_exec_result

        # Mock the conversation query execution (for ownership check)
        mock_conversation_exec_result = MagicMock()
        mock_conversation_exec_result.first.return_value = mock_conversation
        # Need to set up exec to return different results based on query
        mock_session_instance.exec.side_effect = [mock_message_exec_result, mock_conversation_exec_result]

        # Call the method
        result = service.delete_message(mock_session_instance, message_id, user_id)

        # Assertions
        mock_session_instance.delete.assert_called_once_with(mock_message)
        mock_session_instance.commit.assert_called_once()
        assert result is True
