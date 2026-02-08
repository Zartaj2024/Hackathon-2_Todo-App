"""
Message service for the AI-Powered Chatbot feature.
Provides CRUD operations for messages with proper conversation ownership validation.
"""

from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime

from models.message import (
    Message,
    MessageCreate,
    MessageRead,
    MessageUpdate
)
from models.conversation import Conversation


class MessageService:
    """
    Service class for managing messages.
    """

    def create_message(
        self, db_session: Session, message_data: MessageCreate
    ) -> MessageRead:
        """
        Create a new message with conversation_id validation.

        Args:
            db_session: Database session
            message_data: Data for creating the message

        Returns:
            MessageRead: Created message data
        """
        # Validate that the conversation exists and belongs to the user
        conversation_statement = select(Conversation).where(
            Conversation.id == message_data.conversation_id
        )
        conversation = db_session.exec(conversation_statement).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

        # Create the Message object directly with explicit field assignment to avoid inheritance issues
        message = Message()
        message.conversation_id = message_data.conversation_id
        message.role = message_data.role
        message.content = message_data.content
        message.message_type = message_data.message_type
        message.metadata_json = message_data.metadata_json

        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        return MessageRead.model_validate(message)

    def get_messages_by_conversation(
        self, db_session: Session, conversation_id: str, user_id: str,
        limit: int = 50, offset: int = 0
    ) -> List[MessageRead]:
        """
        Get all messages for a conversation with ordering and pagination.

        Args:
            db_session: Database session
            conversation_id: ID of the conversation whose messages to retrieve
            user_id: ID of the requesting user (for validation)
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List[MessageRead]: List of messages in the conversation
        """
        # First validate that the conversation belongs to the user
        conversation_statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(conversation_statement).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or you don't have permission to access it"
            )

        # Get messages for the conversation
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .offset(offset)
            .limit(limit)
            .order_by(Message.timestamp.asc())  # Order messages chronologically
        )
        messages = db_session.exec(statement).all()

        return [MessageRead.model_validate(msg) for msg in messages]

    def update_message(
        self, db_session: Session, message_id: str, user_id: str,
        message_update: MessageUpdate
    ) -> MessageRead:
        """
        Update a message with user ownership validation through conversation.

        Args:
            db_session: Database session
            message_id: ID of the message to update
            user_id: ID of the requesting user
            message_update: Updated message data

        Returns:
            MessageRead: Updated message data
        """
        # Get the message and its associated conversation
        message_statement = select(Message).where(Message.id == message_id)
        message = db_session.exec(message_statement).first()

        if not message:
            raise HTTPException(
                status_code=404,
                detail="Message not found"
            )

        # Verify that the conversation belongs to the user
        conversation_statement = select(Conversation).where(
            Conversation.id == message.conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(conversation_statement).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Message not found or you don't have permission to modify it"
            )

        # Update the message with provided fields
        update_data = message_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(message, field, value)

        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)

        return MessageRead.model_validate(message)

    def delete_message(
        self, db_session: Session, message_id: str, user_id: str
    ) -> bool:
        """
        Delete a message with user ownership validation through conversation.

        Args:
            db_session: Database session
            message_id: ID of the message to delete
            user_id: ID of the requesting user

        Returns:
            bool: True if deletion was successful
        """
        # Get the message and its associated conversation
        message_statement = select(Message).where(Message.id == message_id)
        message = db_session.exec(message_statement).first()

        if not message:
            raise HTTPException(
                status_code=404,
                detail="Message not found"
            )

        # Verify that the conversation belongs to the user
        conversation_statement = select(Conversation).where(
            Conversation.id == message.conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(conversation_statement).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Message not found or you don't have permission to delete it"
            )

        # Delete the message
        db_session.delete(message)
        db_session.commit()
        return True


# Global instance of the service
message_service = MessageService()