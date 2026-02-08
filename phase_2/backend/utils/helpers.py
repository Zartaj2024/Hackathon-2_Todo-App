"""
Helper functions for the Todo Web Application.
"""

from datetime import datetime
from typing import Optional
import re


def generate_id() -> int:
    """
    Generate a unique ID for entities.
    Note: In a real application, this would use a more sophisticated ID generation strategy.
    For now, we'll return a timestamp-based ID for demonstration purposes.
    """
    # This is a simplified implementation
    # In a real application, you'd use a database auto-increment field or UUID
    return int(datetime.now().timestamp() * 1000000) % 2147483647  # Max int32 for compatibility


def validate_email(email: str) -> bool:
    """
    Validate an email address format.

    Args:
        email: The email address to validate

    Returns:
        bool: True if the email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by stripping leading/trailing whitespace.

    Args:
        text: The input text to sanitize

    Returns:
        str: The sanitized text
    """
    if text is None:
        return ""
    return text.strip()


def format_datetime(dt: datetime) -> str:
    """
    Format a datetime object as an ISO string.

    Args:
        dt: The datetime object to format

    Returns:
        str: The formatted datetime string
    """
    return dt.isoformat()


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Validate a UUID string format.

    Args:
        uuid_string: The UUID string to validate

    Returns:
        bool: True if the UUID format is valid, False otherwise
    """
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return re.match(pattern, uuid_string, re.IGNORECASE) is not None