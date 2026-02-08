from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """
    Model for individual chat messages.
    """
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    """
    messages: List[ChatMessage]
    conversation_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatErrorResponse(BaseModel):
    """
    Error response model for chat endpoint.
    """
    success: bool = False
    error: str
    timestamp: datetime = Field(default_factory=datetime.now)