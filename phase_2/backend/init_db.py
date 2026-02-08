"""
Database initialization script for local development.
"""

from sqlmodel import create_engine, SQLModel
from models.user import User
from models.task import Task
from config import settings

def init_database():
    """Initialize the database with required tables."""
    print("Initializing database...")

    # Create engine with the same settings as the main app
    engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

    # Create all tables
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()