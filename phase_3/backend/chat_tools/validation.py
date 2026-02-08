"""
Common validation and sanitization functions for MCP tools.
Implements input validation and sanitization as specified in mcp-tools.md.
"""

import re
from typing import Any, Dict, List
from datetime import date


def sanitize_input(text: str) -> str:
    """
    Sanitize text input by removing potentially harmful content.

    Args:
        text: Input text to sanitize

    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Remove control characters except whitespace
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    return sanitized


def validate_title(title: str) -> bool:
    """
    Validate task title based on requirements.

    Args:
        title: Title to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if not isinstance(title, str):
        raise ValueError("Title must be a string")

    if len(title) < 1 or len(title) > 255:
        raise ValueError("Title must be between 1 and 255 characters")

    # Check for potentially harmful content
    if re.search(r'[<>{}]', title):
        raise ValueError("Title contains invalid characters")

    return True


def validate_description(description: str) -> bool:
    """
    Validate task description based on requirements.

    Args:
        description: Description to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if description is None:
        return True

    if not isinstance(description, str):
        raise ValueError("Description must be a string or None")

    if len(description) > 1000:
        raise ValueError("Description must be less than 1000 characters")

    # Check for potentially harmful content
    if re.search(r'<script', description, re.IGNORECASE):
        raise ValueError("Description contains invalid content")

    return True


def validate_priority(priority: str) -> bool:
    """
    Validate task priority based on requirements.

    Args:
        priority: Priority to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if priority is None:
        return True

    if not isinstance(priority, str):
        raise ValueError("Priority must be a string or None")

    valid_priorities = ["low", "medium", "high"]
    if priority.lower() not in valid_priorities:
        raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")

    return True


def validate_date_format(date_str: str) -> bool:
    """
    Validate date string format (YYYY-MM-DD).

    Args:
        date_str: Date string to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if date_str is None:
        return True

    if not isinstance(date_str, str):
        raise ValueError("Date must be a string or None")

    import re
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        raise ValueError("Date must be in YYYY-MM-DD format")

    # Additional validation to check if it's a real date
    try:
        date.fromisoformat(date_str)
    except ValueError:
        raise ValueError("Invalid date")

    return True


def validate_task_id(task_id: int) -> bool:
    """
    Validate task ID is a positive integer.

    Args:
        task_id: Task ID to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if not isinstance(task_id, int):
        raise ValueError("Task ID must be an integer")

    if task_id <= 0:
        raise ValueError("Task ID must be a positive integer")

    return True


def validate_status_filter(status: str) -> bool:
    """
    Validate status filter for listing tasks.

    Args:
        status: Status filter to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if status is None:
        return True

    if not isinstance(status, str):
        raise ValueError("Status must be a string or None")

    valid_statuses = ["all", "completed", "pending"]
    if status.lower() not in valid_statuses:
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

    return True


def validate_limit(limit: int) -> bool:
    """
    Validate limit for pagination.

    Args:
        limit: Limit to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if limit is None:
        return True

    if not isinstance(limit, int):
        raise ValueError("Limit must be an integer or None")

    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")

    return True


def validate_offset(offset: int) -> bool:
    """
    Validate offset for pagination.

    Args:
        offset: Offset to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if offset is None:
        return True

    if not isinstance(offset, int):
        raise ValueError("Offset must be an integer or None")

    if offset < 0:
        raise ValueError("Offset must be greater than or equal to 0")

    return True


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format.

    Args:
        user_id: User ID to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if not isinstance(user_id, str):
        raise ValueError("User ID must be a string")

    if len(user_id) < 1 or len(user_id) > 255:
        raise ValueError("User ID must be between 1 and 255 characters")

    # Basic validation to ensure it's a reasonable user ID format
    # (allows alphanumeric, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        raise ValueError("User ID contains invalid characters")

    return True


def validate_boolean(value: bool) -> bool:
    """
    Validate boolean value.

    Args:
        value: Value to validate

    Returns:
        bool: True if valid, raises ValueError if not
    """
    if value is None:
        return True

    if not isinstance(value, bool):
        raise ValueError("Value must be a boolean or None")

    return True