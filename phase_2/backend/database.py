"""
Database connection and session management for the Todo Web Application.
"""

import logging
from sqlmodel import create_engine, Session
from typing import Generator
from config import settings

# Set up logging
logger = logging.getLogger(__name__)


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Set to True to see SQL queries in development
    pool_pre_ping=True,  # Verify connections before use
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session with error handling.

    Yields:
        Session: A database session for use in API endpoints.
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Database session error: {str(e)}", exc_info=True)
        raise


def create_db_and_tables():
    """
    Create database tables based on SQLModel models with error handling.
    """
    try:
        logger.info("Starting database table creation...")

        # Import all models to ensure they're registered with SQLModel
        from models.user import User  # noqa: F401
        from models.task import Task  # noqa: F401
        from models.conversation import Conversation  # noqa: F401
        from models.message import Message  # noqa: F401
        from chat_models.chat import ChatMessage, ChatRequest, ChatResponse  # noqa: F401

        # Import SQLModel to create all tables
        from sqlmodel import SQLModel

        # Test the database connection first
        with Session(engine) as session:
            logger.info("Database connection successful")
        
        # Create all tables
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}", exc_info=True)
        raise