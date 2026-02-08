"""
User model for the Todo Web Application.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid


class UserBase(SQLModel):
    """
    Base class for User model containing shared attributes.
    """
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: str = Field(nullable=False, min_length=1, max_length=255)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """
    User entity representing an authenticated user of the system.

    Attributes:
        id: Unique identifier for the user
        email: User's email address (unique)
        name: User's display name
        created_at: Timestamp when user account was created
        updated_at: Timestamp when user account was last updated
        is_active: Whether the account is active (default: true)
    """
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password: str = Field(nullable=False, min_length=8, max_length=255)  # Add password field to the User model with constraints
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")

    # Relationship to conversations
    conversations: list["Conversation"] = Relationship(back_populates="user")

    def __str__(self):
        return f"User(id={self.id}, email={self.email}, name={self.name})"

    def __repr__(self):
        return self.__str__()

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "uuid-string",
                "email": "user@example.com",
                "name": "John Doe",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }


class UserRead(UserBase):
    """
    Schema for reading user data, excluding sensitive information.
    """
    id: str
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str = Field(min_length=8, max_length=128)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "securePassword123"
            }
        }


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = Field(None, max_length=255)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "updated@example.com",
                "name": "Updated Name",
                "is_active": True,
                "password": "newSecurePassword123"
            }
        }