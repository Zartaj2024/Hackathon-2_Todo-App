"""
Enhanced database connection module for the Todo Web Application with comprehensive error handling.
"""

from sqlmodel import create_engine, Session
from typing import Generator
import logging
from contextlib import contextmanager
from config import settings
import time
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError, InvalidRequestError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnectionManager:
    """
    Enhanced database connection manager with comprehensive error handling and retry logic.
    """

    def __init__(self):
        self.engine = None
        self._initialize_engine()

    def _initialize_engine(self):
        """Initialize the database engine with proper error handling."""
        try:
            self.engine = create_engine(
                settings.DATABASE_URL,
                echo=settings.DEBUG,
                pool_pre_ping=True,
                pool_recycle=300,  # Recycle connections every 5 minutes
                pool_size=10,
                max_overflow=20,
                connect_args={
                    "connect_timeout": 10,  # 10 second connection timeout
                }
            )
            logger.info("Database engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """
        Test the database connection with comprehensive error handling.

        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            from sqlalchemy import text
            with self.engine.connect() as connection:
                # Execute a simple query to test the connection
                result = connection.execute(text("SELECT 1"))
                logger.info("Database connection test successful")
                return True
        except DisconnectionError as e:
            logger.error(f"Database disconnection error: {str(e)}")
            # Attempt to reinitialize the engine
            try:
                self._initialize_engine()
                logger.info("Database engine reinitialized after disconnection")
                return True
            except Exception as reinit_error:
                logger.error(f"Failed to reinitialize database engine: {str(reinit_error)}")
                return False
        except InvalidRequestError as e:
            logger.error(f"Invalid request error: {str(e)}")
            return False
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error during connection test: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {str(e)}")
            return False

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager to get a database session with comprehensive error handling.

        Yields:
            Session: A database session for use in API endpoints.
        """
        session = None
        try:
            session = Session(self.engine)
            yield session
            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            if session:
                try:
                    session.close()
                except Exception as close_error:
                    logger.error(f"Error closing session: {str(close_error)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((SQLAlchemyError, DisconnectionError))
    )
    def execute_with_retry(self, func, *args, **kwargs):
        """
        Execute a database operation with retry logic.

        Args:
            func: The function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the function execution
        """
        try:
            return func(*args, **kwargs)
        except (SQLAlchemyError, DisconnectionError) as e:
            logger.warning(f"Database operation failed, retrying... Error: {str(e)}")
            raise  # Re-raise to trigger retry


# Global instance
db_manager = DatabaseConnectionManager()


@contextmanager
def get_enhanced_session() -> Generator[Session, None, None]:
    """
    Context manager to get an enhanced database session with error handling.

    Yields:
        Session: A database session for use in API endpoints.
    """
    with db_manager.get_session() as session:
        yield session


def create_db_and_tables():
    """
    Create database tables based on SQLModel models with error handling.
    """
    try:
        from .models.user import User  # noqa: F401
        from .models.task import Task  # noqa: F401

        # Import all models here to ensure they're registered with SQLModel
        from sqlmodel import SQLModel

        # Create all tables
        SQLModel.metadata.create_all(db_manager.engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise


def health_check() -> dict:
    """
    Perform a health check on the database connection.

    Returns:
        dict: Health check results
    """
    try:
        is_connected = db_manager.test_connection()
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "database": "connected" if is_connected else "disconnected",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e),
            "timestamp": time.time()
        }


# Test connection on module load
if __name__ != "__main__":
    try:
        db_manager.test_connection()
    except Exception as e:
        logger.error(f"Warning: Database connection test failed on module load: {str(e)}")