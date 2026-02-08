"""
Test script for Neon DB connection with comprehensive error handling.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_enhanced import db_manager, health_check
from models.user import User
from sqlmodel import select
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_basic_connection():
    """Test basic database connection."""
    logger.info("Testing basic database connection...")
    try:
        # Test connection using SQLAlchemy text
        from sqlalchemy import text

        with db_manager.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()

        if row:
            logger.info("✓ Basic connection test passed")
            return True
        else:
            logger.error("✗ Basic connection test failed - no result returned")
            return False
    except Exception as e:
        logger.error(f"✗ Basic connection test raised exception: {str(e)}")
        return False


def test_health_check():
    """Test database health check."""
    logger.info("Testing database health check...")
    try:
        health_result = health_check()
        logger.info(f"Health check result: {health_result}")

        if health_result["status"] == "healthy":
            logger.info("✓ Health check passed")
            return True
        else:
            logger.error("✗ Health check failed")
            return False
    except Exception as e:
        logger.error(f"✗ Health check raised exception: {str(e)}")
        return False


def test_query_execution():
    """Test basic query execution."""
    logger.info("Testing basic query execution...")
    try:
        # First, create the tables if they don't exist
        from database import create_db_and_tables
        create_db_and_tables()

        with db_manager.get_session() as session:
            # Try to count users (should work even if table is empty)
            statement = select(User)
            results = session.exec(statement)
            users = results.all()
            logger.info(f"✓ Query execution passed - Found {len(users)} users")
            return True
    except ImportError:
        # If there's an import error, try direct import
        try:
            from .database import create_db_and_tables
            create_db_and_tables()

            with db_manager.get_session() as session:
                # Try to count users (should work even if table is empty)
                statement = select(User)
                results = session.exec(statement)
                users = results.all()
                logger.info(f"✓ Query execution passed - Found {len(users)} users")
                return True
        except Exception as e:
            logger.error(f"✗ Query execution failed: {str(e)}")
            return False
    except Exception as e:
        logger.error(f"✗ Query execution failed: {str(e)}")
        return False


def test_connection_pool():
    """Test connection pool functionality."""
    logger.info("Testing connection pool...")
    try:
        # Test multiple sequential connections
        from sqlalchemy import text

        for i in range(3):
            with db_manager.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                row = result.fetchone()
                logger.debug(f"Connection {i+1} successful: {row}")

        logger.info("✓ Connection pool test passed")
        return True
    except Exception as e:
        logger.error(f"✗ Connection pool test failed: {str(e)}")
        return False


def run_all_tests():
    """Run all connection tests."""
    logger.info("Starting comprehensive Neon DB connection tests...")

    tests = [
        ("Basic Connection", test_basic_connection),
        ("Health Check", test_health_check),
        ("Query Execution", test_query_execution),
        ("Connection Pool", test_connection_pool),
    ]

    results = {}
    for test_name, test_func in tests:
        logger.info(f"\n--- Running {test_name} ---")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {str(e)}")
            results[test_name] = False

    # Summary
    logger.info("\n=== Test Summary ===")
    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")

    logger.info(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All tests passed! Neon DB connection is working properly.")
        return True
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)