"""
Message model for the AI-Powered Chatbot feature.
"""

from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from .conversation import Conversation
    from .user import User  # Needed for relationship validation
    from .task import Task  # Needed for relationship validation


def generate_uuid():
    """
    Generate a UUID string for use as a default value in models.
    """
    return str(uuid4())


class MessageRole(str, enum.Enum):
    """
    Enum for message roles.
    """
    USER = "user"
    ASSISTANT = "assistant"


class MessageType(str, enum.Enum):
    """
    Enum for message types.
    """
    TEXT = "text"
    COMMAND = "command"
    RESPONSE = "response"
    ERROR = "error"


class MessageBase(SQLModel):
    """
    Base class for Message model containing shared attributes.
    """
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False, max_length=5000)  # Allow longer messages
    message_type: MessageType = Field(default=MessageType.TEXT)
    metadata_json: Optional[str] = Field(default=None, max_length=10000)  # Store as JSON string


class Message(MessageBase, table=True):
    """
    Message entity representing a chat message in a conversation.

    Attributes:
        id: Unique identifier for the message (UUID)
        conversation_id: Reference to the conversation
        role: Either "user" or "assistant"
        content: The actual message content
        timestamp: When the message was sent
        message_type: Either "text", "command", "response", "error"
        metadata: Additional data like tool calls, parameters (stored as JSON string)
    """
    __tablename__ = "messages"

    id: str = Field(default_factory=generate_uuid, primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", nullable=False, index=True)

    # Relationship
    conversation: "Conversation" = Relationship(back_populates="messages")

    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def __str__(self):
        return f"Message(id={self.id}, conversation_id={self.conversation_id}, role={self.role})"

    def __repr__(self):
        return self.__str__()

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "uuid-string",
                "conversation_id": "conversation-uuid-string",
                "role": "user",
                "content": "Hello, how can I add a task?",
                "timestamp": "2023-01-01T00:00:00Z",
                "message_type": "text",
                "metadata": '{"tool_calls": []}'
            }
        }


class MessageRead(MessageBase):
    """
    Schema for reading message data.
    """
    id: str
    conversation_id: str
    timestamp: datetime


class MessageCreate(MessageBase):
    """
    Schema for creating a new message.
    """
    conversation_id: str = Field(..., min_length=1, max_length=255)
    role: MessageRole

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conversation-id-string",
                "role": "user",
                "content": "Add a new task called 'Buy groceries'",
                "message_type": "command"
            }
        }


class MessageUpdate(SQLModel):
    """
    Schema for updating message information.
    """
    content: Optional[str] = Field(None, max_length=5000)
    message_type: Optional[MessageType] = None
    metadata_json: Optional[str] = Field(None, max_length=10000)

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Updated message content",
                "message_type": "response"
            }
        }