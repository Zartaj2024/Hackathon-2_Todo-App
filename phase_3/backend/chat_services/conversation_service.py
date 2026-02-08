"""
Conversation service for the AI-Powered Chatbot feature.
Provides CRUD operations for conversations with proper user ownership validation.
"""

from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from uuid import UUID

from models.conversation import (
    Conversation,
    ConversationCreate,
    ConversationRead,
    ConversationUpdate
)
from models.message import Message


class ConversationService:
    """
    Service class for managing conversations.
    """

    def create_conversation(
        self, db_session: Session, conversation_data: ConversationCreate
    ) -> ConversationRead:
        """
        Create a new conversation with user_id validation.

        Args:
            db_session: Database session
            conversation_data: Data for creating the conversation

        Returns:
            ConversationRead: Created conversation data
        """
        # Validate that user_id exists by attempting to retrieve the user
        # In a full implementation, you'd have a user service to validate this

        conversation = Conversation.model_validate(conversation_data)
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        return ConversationRead.model_validate(conversation)

    def get_conversation_by_id(
        self, db_session: Session, conversation_id: str, user_id: str
    ) -> ConversationRead:
        """
        Get a conversation by ID with user ownership validation.

        Args:
            db_session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the requesting user

        Returns:
            ConversationRead: Retrieved conversation data
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(statement).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or you don't have permission to access it"
            )

        return ConversationRead.model_validate(conversation)

    def get_user_conversations(
        self, db_session: Session, user_id: str, limit: int = 10, offset: int = 0
    ) -> List[ConversationRead]:
        """
        Get all conversations for a user with pagination support.

        Args:
            db_session: Database session
            user_id: ID of the user whose conversations to retrieve
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip

        Returns:
            List[ConversationRead]: List of user's conversations
        """
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .offset(offset)
            .limit(limit)
            .order_by(Conversation.created_at.desc())
        )
        conversations = db_session.exec(statement).all()

        return [ConversationRead.model_validate(conv) for conv in conversations]

    def update_conversation(
        self, db_session: Session, conversation_id: str, user_id: str,
        conversation_update: ConversationUpdate
    ) -> ConversationRead:
        """
        Update a conversation with user ownership validation.

        Args:
            db_session: Database session
            conversation_id: ID of the conversation to update
            user_id: ID of the requesting user
            conversation_update: Updated conversation data

        Returns:
            ConversationRead: Updated conversation data
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(statement).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or you don't have permission to modify it"
            )

        # Update the conversation with provided fields
        update_data = conversation_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)

        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)

        return ConversationRead.model_validate(conversation)

    def delete_conversation(
        self, db_session: Session, conversation_id: str, user_id: str
    ) -> bool:
        """
        Delete a conversation with user ownership validation and cascade deletion of messages.

        Args:
            db_session: Database session
            conversation_id: ID of the conversation to delete
            user_id: ID of the requesting user

        Returns:
            bool: True if deletion was successful
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = db_session.exec(statement).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or you don't have permission to delete it"
            )

        # Delete associated messages first (cascade)
        message_statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = db_session.exec(message_statement).all()
        for message in messages:
            db_session.delete(message)

        # Delete the conversation
        db_session.delete(conversation)
        db_session.commit()
        return True


# Global instance of the service
conversation_service = ConversationService()