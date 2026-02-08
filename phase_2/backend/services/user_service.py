"""
Business logic for user operations in the Todo Web Application.
"""

from sqlmodel import Session, select
from typing import Optional

from models.user import User


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.

    Args:
        session: Database session
        email: Email address to search for

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """
    Get a user by their ID.

    Args:
        session: Database session
        user_id: User ID to search for

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()


def create_user(session: Session, user: User) -> User:
    """
    Create a new user.

    Args:
        session: Database session
        user: User object to create

    Returns:
        User: Created user object
    """
    session.add(user)
    session.commit()
    session.refresh(user)
    return user