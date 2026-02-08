"""
Conversation model for the AI-Powered Chatbot feature.
"""

from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from .user import User
    from .message import Message
    from .task import Task  # Needed for relationship validation


def generate_uuid():
    """
    Generate a UUID string for use as a default value in models.
    """
    return str(uuid4())


class ConversationStatus(str, enum.Enum):
    """
    Enum for conversation status.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"


class ConversationBase(SQLModel):
    """
    Base class for Conversation model containing shared attributes.
    """
    title: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)


class Conversation(ConversationBase, table=True):
    """
    Conversation entity representing a chat session.

    Attributes:
        id: Unique identifier for the conversation (UUID)
        user_id: Reference to the owning user
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last updated
        title: Optional title auto-generated from first message
        is_active: Whether conversation is ongoing
    """
    __tablename__ = "conversations"

    id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def __str__(self):
        return f"Conversation(id={self.id}, user_id={self.user_id}, is_active={self.is_active})"

    def __repr__(self):
        return self.__str__()

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "uuid-string",
                "user_id": "user-uuid-string",
                "title": "Task management discussion",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }


class ConversationRead(ConversationBase):
    """
    Schema for reading conversation data.
    """
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class ConversationCreate(ConversationBase):
    """
    Schema for creating a new conversation.
    """
    user_id: str = Field(..., min_length=1, max_length=255)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "New conversation",
                "user_id": "user-id-string"
            }
        }


class ConversationUpdate(SQLModel):
    """
    Schema for updating conversation information.
    """
    title: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated conversation title",
                "is_active": False
            }
        }