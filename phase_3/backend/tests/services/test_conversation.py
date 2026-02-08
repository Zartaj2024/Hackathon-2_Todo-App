"""
Unit tests for the conversation service.
Tests the conversation service functionality for CRUD operations.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from uuid import uuid4

from chat_services.conversation_service import ConversationService
from models.conversation import ConversationCreate


def test_create_conversation():
    """Test creating a new conversation."""
    # Create a mock conversation service
    service = ConversationService()

    # Mock data
    user_id = "test-user-id"
    conversation_data = ConversationCreate(
        title="Test Conversation",
        user_id=user_id
    )

    # Create a mock conversation object
    mock_conversation = MagicMock()
    mock_conversation.id = str(uuid4())
    mock_conversation.title = "Test Conversation"
    mock_conversation.user_id = user_id
    mock_conversation.is_active = True

    with patch('chat_services.conversation_service.Session') as mock_session_class:
        # Configure the mock session
        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the add, commit, and refresh methods
        mock_session_instance.add = MagicMock()
        mock_session_instance.commit = MagicMock()
        mock_session_instance.refresh = MagicMock()

        # Mock the conversation object after validation
        with patch('chat_services.conversation_service.Conversation.model_validate') as mock_model_validate:
            mock_model_validate.return_value = mock_conversation

            # Call the method
            result = service.create_conversation(mock_session_instance, conversation_data)

            # Assertions
            mock_session_instance.add.assert_called_once_with(mock_conversation)
            mock_session_instance.commit.assert_called_once()
            mock_session_instance.refresh.assert_called_once_with(mock_conversation)
            mock_model_validate.assert_called_once_with(conversation_data)


def test_get_conversation_by_id_success():
    """Test getting a conversation by ID successfully."""
    service = ConversationService()

    conversation_id = str(uuid4())
    user_id = "test-user-id"

    mock_conversation = MagicMock()
    mock_conversation.id = conversation_id
    mock_conversation.user_id = user_id
    mock_conversation.title = "Test Conversation"

    with patch('chat_services.conversation_service.Session') as mock_session_class, \
         patch('chat_services.conversation_service.select') as mock_select, \
         patch('chat_services.conversation_service.Conversation') as mock_conversation_model:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the query execution
        mock_exec_result = MagicMock()
        mock_exec_result.first.return_value = mock_conversation
        mock_session_instance.exec.return_value = mock_exec_result

        # Mock the ConversationRead model validation
        with patch('chat_services.conversation_service.ConversationRead.model_validate') as mock_model_validate:
            mock_model_validate.return_value = MagicMock()

            # Call the method
            result = service.get_conversation_by_id(mock_session_instance, conversation_id, user_id)

            # Assertions
            mock_select.assert_called_once()
            mock_exec_result.first.assert_called_once()
            mock_model_validate.assert_called_once_with(mock_conversation)


def test_get_conversation_by_id_not_found():
    """Test getting a conversation that doesn't exist."""
    service = ConversationService()

    conversation_id = str(uuid4())
    user_id = "test-user-id"

    with patch('chat_services.conversation_service.Session') as mock_session_class, \
         patch('chat_services.conversation_service.select') as mock_select:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the query execution returning None
        mock_exec_result = MagicMock()
        mock_exec_result.first.return_value = None
        mock_session_instance.exec.return_value = mock_exec_result

        # Expect an HTTPException to be raised
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            service.get_conversation_by_id(mock_session_instance, conversation_id, user_id)

        assert exc_info.value.status_code == 404
        assert "Conversation not found" in exc_info.value.detail


def test_get_user_conversations():
    """Test getting all conversations for a user."""
    service = ConversationService()

    user_id = "test-user-id"

    # Create mock conversations
    mock_conv1 = MagicMock()
    mock_conv1.id = str(uuid4())
    mock_conv1.user_id = user_id
    mock_conv1.title = "Conversation 1"

    mock_conv2 = MagicMock()
    mock_conv2.id = str(uuid4())
    mock_conv2.user_id = user_id
    mock_conv2.title = "Conversation 2"

    mock_conversations = [mock_conv1, mock_conv2]

    with patch('chat_services.conversation_service.Session') as mock_session_class, \
         patch('chat_services.conversation_service.select') as mock_select:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the query execution
        mock_exec_result = MagicMock()
        mock_exec_result.all.return_value = mock_conversations
        mock_session_instance.exec.return_value = mock_exec_result

        # Mock the ConversationRead model validation
        with patch('chat_services.conversation_service.ConversationRead.model_validate') as mock_model_validate:
            mock_model_validate.side_effect = lambda x: MagicMock()  # Return mock for each conversion

            # Call the method
            result = service.get_user_conversations(mock_session_instance, user_id)

            # Assertions
            mock_select.assert_called_once()
            mock_exec_result.all.assert_called_once()
            assert mock_model_validate.call_count == len(mock_conversations)


def test_update_conversation():
    """Test updating a conversation."""
    service = ConversationService()

    conversation_id = str(uuid4())
    user_id = "test-user-id"

    mock_conversation = MagicMock()
    mock_conversation.id = conversation_id
    mock_conversation.user_id = user_id
    mock_conversation.title = "Old Title"

    mock_update_data = MagicMock()
    mock_update_data.model_dump.return_value = {"title": "New Title"}

    with patch('chat_services.conversation_service.Session') as mock_session_class, \
         patch('chat_services.conversation_service.select') as mock_select:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # Mock the query execution
        mock_exec_result = MagicMock()
        mock_exec_result.first.return_value = mock_conversation
        mock_session_instance.exec.return_value = mock_exec_result

        # Mock the ConversationUpdate object
        mock_conversation_update = MagicMock()
        mock_conversation_update.model_dump.return_value = {"title": "New Title"}

        # Mock the ConversationRead model validation
        with patch('chat_services.conversation_service.ConversationRead.model_validate') as mock_model_validate:
            mock_model_validate.return_value = MagicMock()

            # Call the method
            result = service.update_conversation(mock_session_instance, conversation_id, user_id, mock_conversation_update)

            # Assertions
            mock_select.assert_called_once()
            mock_exec_result.first.assert_called_once()
            assert mock_conversation.title == "New Title"
            mock_session_instance.add.assert_called_once_with(mock_conversation)
            mock_session_instance.commit.assert_called_once()
            mock_session_instance.refresh.assert_called_once_with(mock_conversation)


def test_delete_conversation():
    """Test deleting a conversation."""
    service = ConversationService()

    conversation_id = str(uuid4())
    user_id = "test-user-id"

    mock_conversation = MagicMock()
    mock_conversation.id = conversation_id
    mock_conversation.user_id = user_id

    with patch('chat_services.conversation_service.Session') as mock_session_class, \
         patch('chat_services.conversation_service.select') as mock_select:

        mock_session_instance = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session_instance
        mock_session_class.return_value.__exit__.return_value = None

        # First call: Get conversation by ID (for ownership check)
        mock_conversation_exec_result = MagicMock()
        mock_conversation_exec_result.first.return_value = mock_conversation

        # Second call: Get messages (for cascade deletion)
        mock_message_exec_result = MagicMock()
        mock_message_exec_result.all.return_value = []

        # Third call: Delete the conversation
        mock_delete_exec_result = MagicMock()

        # Configure exec to return different results on subsequent calls
        mock_session_instance.exec.side_effect = [
            mock_conversation_exec_result,  # For conversation query
            mock_message_exec_result,      # For message query
            mock_delete_exec_result        # For delete query
        ]

        # Mock the delete and commit methods
        mock_session_instance.delete = MagicMock()
        mock_session_instance.commit = MagicMock()

        # Call the method
        result = service.delete_conversation(mock_session_instance, conversation_id, user_id)

        # Assertions
        assert mock_session_instance.delete.called
        mock_session_instance.commit.assert_called_once()
        assert result is True
