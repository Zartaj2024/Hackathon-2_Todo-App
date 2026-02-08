"""
Task model for the Todo Console Application.

This module defines the Task entity with all required attributes
and validation as specified in the requirements.
"""

from typing import Optional
import logging


class Task:
    """
    Represents a single todo item with the following attributes:
    - id: Unique identifier (auto-generated, numeric)
    - title: Required string that describes the task
    - description: Optional string with additional details
    - completed: Boolean indicating if the task is finished
    """

    def __init__(self, task_id: int, title: str, description: Optional[str] = None, completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Required title of the task
            description (str, optional): Optional description of the task
            completed (bool): Whether the task is completed, defaults to False
        """
        self.id = self._validate_id(task_id)
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.completed = completed

    def _validate_id(self, task_id: int) -> int:
        """
        Validate that the ID is a positive integer.

        Args:
            task_id (int): The ID to validate

        Returns:
            int: The validated ID

        Raises:
            ValueError: If the ID is not a positive integer
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got {task_id}")
        return task_id

    def _validate_title(self, title: str) -> str:
        """
        Validate that the title is not empty or just whitespace.

        Args:
            title (str): The title to validate

        Returns:
            str: The validated title

        Raises:
            ValueError: If the title is empty or contains only whitespace
        """
        if not isinstance(title, str):
            raise ValueError(f"Task title must be a string, got {type(title).__name__}")

        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or contain only whitespace")

        # Validate length to handle extremely long text inputs (edge case)
        if len(title) > 1000:
            raise ValueError("Task title cannot exceed 1000 characters")

        return title.strip()

    def _validate_description(self, description: Optional[str]) -> str:
        """
        Validate the description field.

        Args:
            description (str, optional): The description to validate

        Returns:
            str: The validated description (or empty string if None)
        """
        if description is None:
            return ""

        if not isinstance(description, str):
            raise ValueError(f"Task description must be a string, got {type(description).__name__}")

        # Validate length to handle extremely long text inputs (edge case)
        if len(description) > 5000:
            raise ValueError("Task description cannot exceed 5000 characters")

        return description

    def __str__(self) -> str:
        """
        String representation of the task for display purposes.

        Returns:
            str: Formatted string representation of the task
        """
        status = "✓" if self.completed else "○"
        desc = f"\n   {self.description}" if self.description else ""
        return f"[{status}] {self.id}. {self.title}{desc}"

    def __repr__(self) -> str:
        """
        Developer-friendly representation of the task.

        Returns:
            str: Detailed representation of the task object
        """
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"

    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary containing all task attributes
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Task instance from a dictionary.

        Args:
            data (dict): Dictionary containing task attributes

        Returns:
            Task: New Task instance
        """
        try:
            return cls(
                task_id=data["id"],
                title=data["title"],
                description=data.get("description"),
                completed=data.get("completed", False)
            )
        except KeyError as e:
            logging.error(f"Missing required field in task data: {e}")
            raise ValueError(f"Missing required field in task data: {e}")
        except Exception as e:
            logging.error(f"Error creating task from dictionary: {e}")
            raise ValueError(f"Invalid task data: {e}")