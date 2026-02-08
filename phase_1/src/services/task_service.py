"""
Task service for the Todo Console Application.

This module implements the business logic for task operations
including Create, Read, Update, Delete, and Toggle completion.
It connects to the shared backend API to sync with the web application.
"""

from typing import List, Optional, Dict, Any
import logging
from src.models.task import Task
from .api_client import APIClient


class MockAPIClient:
    """
    Mock API client for testing purposes that simulates API behavior without making actual requests.
    """
    
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
    
    def set_auth_token(self, token: str):
        """Set the authentication token for API requests."""
        pass  # No-op for mock
    
    def create_task(self, title: str, description: str = "", completed: bool = False) -> Dict[str, Any]:
        """Create a new task in memory."""
        task_id = self.next_id
        self.next_id += 1
        
        task_data = {
            "id": task_id,
            "title": title,
            "description": description,
            "completed": completed
        }
        
        self.tasks[task_id] = task_data
        return {"task": task_data}
    
    def get_tasks(self) -> Dict[str, Any]:
        """Get all tasks from memory."""
        return {"tasks": list(self.tasks.values())}
    
    def get_task(self, task_id: int) -> Dict[str, Any]:
        """Get a specific task by ID from memory."""
        # Handle invalid task_id types that can't be used as dict keys
        try:
            task = self.tasks.get(task_id)
            if task:
                return {"task": task}
        except TypeError:
            # task_id is not hashable (e.g., list, dict)
            pass
        return {}
    
    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
        """Update a task in memory."""
        try:
            if task_id in self.tasks:
                if title is not None:
                    self.tasks[task_id]["title"] = title
                if description is not None:
                    self.tasks[task_id]["description"] = description
                if completed is not None:
                    self.tasks[task_id]["completed"] = completed
                
                return {"task": self.tasks[task_id]}
            return {}
        except TypeError:
            # task_id is not hashable (e.g., list, dict)
            return {}
    
    def toggle_task_completion(self, task_id: int) -> Dict[str, Any]:
        """Toggle the completion status of a task in memory."""
        try:
            if task_id in self.tasks:
                self.tasks[task_id]["completed"] = not self.tasks[task_id]["completed"]
                return {"task": self.tasks[task_id]}
            return {}
        except TypeError:
            # task_id is not hashable (e.g., list, dict)
            return {}
    
    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task from memory."""
        try:
            if task_id in self.tasks:
                del self.tasks[task_id]
                return {"success": True}
            return {"success": False}
        except TypeError:
            # task_id is not hashable (e.g., list, dict)
            return {"success": False}


class TaskService:
    """
    Primary service class for managing tasks with proper error handling.

    This class connects to the shared backend API to sync with the web application.
    """

    def __init__(self, api_base_url: str = "http://localhost:8000", skip_auth: bool = False):
        """Initialize the task service with API connection."""
        if skip_auth:
            self.api_client = MockAPIClient()
        else:
            self.api_client = APIClient(api_base_url)
        self.auth_token = None
        self.skip_auth = skip_auth  # For testing purposes

    def authenticate(self, email: str, password: str) -> bool:
        """
        Authenticate with the backend API.

        Args:
            email: User's email address
            password: User's password

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            response = self.api_client.login_user(email, password)
            self.auth_token = response.get("access_token") or response.get("data", {}).get("access_token")
            if self.auth_token:
                self.api_client.set_auth_token(self.auth_token)
                return True
            return False
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            return False

    def register_and_authenticate(self, email: str, password: str, name: str) -> bool:
        """
        Register a new user and authenticate.

        Args:
            email: User's email address
            password: User's password
            name: User's name

        Returns:
            True if registration and authentication successful, False otherwise
        """
        try:
            response = self.api_client.register_user(email, password, name)
            # After successful registration, log in to get the token
            return self.authenticate(email, password)
        except Exception as e:
            logging.error(f"Registration failed: {e}")
            return False

    def ensure_authenticated(self):
        """Raise an exception if not authenticated."""
        if not self.skip_auth and not self.auth_token:
            raise Exception("Not authenticated. Please log in first.")

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task with auto-generated unique ID via API.

        Args:
            title (str): Required title of the task
            description (str, optional): Optional description of the task

        Returns:
            Task: The newly created task object

        Raises:
            ValueError: If the title is empty or contains only whitespace
            Exception: If not authenticated or API call fails
        """
        self.ensure_authenticated()

        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or contain only whitespace")

        try:
            description = description or ""
            response = self.api_client.create_task(title.strip(), description.strip())

            # Extract task data from response (structure may vary depending on API)
            task_data = response.get("task", response)  # API might return task in a nested object

            # Create Task object from API response
            task = Task(
                task_id=task_data.get("id"),
                title=task_data.get("title", title),
                description=task_data.get("description", description),
                completed=task_data.get("completed", False)
            )
            return task
        except Exception as e:
            logging.error(f"Error creating task: {e}")
            raise ValueError(f"Failed to create task: {e}")

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks with their properties via API.

        Returns:
            List[Task]: List of all tasks in the system
        """
        self.ensure_authenticated()

        try:
            response = self.api_client.get_tasks()

            # Extract tasks data from response (structure may vary depending on API)
            tasks_data = response.get("tasks", response)  # API might return tasks in a nested object

            tasks = []
            if isinstance(tasks_data, list):
                for task_data in tasks_data:
                    task = Task(
                        task_id=task_data.get("id"),
                        title=task_data.get("title", ""),
                        description=task_data.get("description", ""),
                        completed=task_data.get("completed", False)
                    )
                    tasks.append(task)
            elif isinstance(tasks_data, dict) and "tasks" in tasks_data:
                # Handle case where response is like {"tasks": [...]}
                for task_data in tasks_data["tasks"]:
                    task = Task(
                        task_id=task_data.get("id"),
                        title=task_data.get("title", ""),
                        description=task_data.get("description", ""),
                        completed=task_data.get("completed", False)
                    )
                    tasks.append(task)

            return tasks
        except Exception as e:
            logging.error(f"Error retrieving all tasks: {e}")
            raise ValueError(f"Failed to retrieve tasks: {e}")

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by its ID via API.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task if found, otherwise None
        """
        self.ensure_authenticated()

        try:
            response = self.api_client.get_task(task_id)

            # Extract task data from response (structure may vary depending on API)
            task_data = response.get("task", response)  # API might return task in a nested object

            if task_data:
                task = Task(
                    task_id=task_data.get("id"),
                    title=task_data.get("title", ""),
                    description=task_data.get("description", ""),
                    completed=task_data.get("completed", False)
                )
                return task
            return None
        except Exception as e:
            logging.error(f"Error retrieving task with ID {task_id}: {e}")
            raise ValueError(f"Failed to retrieve task with ID {task_id}: {e}")

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task by ID via API.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            Task or None: The updated task if found, otherwise None

        Raises:
            ValueError: If title is provided but is empty or contains only whitespace
        """
        self.ensure_authenticated()

        # Prepare update data
        update_data = {}
        if title is not None:
            # Validate that title is a string before calling strip
            if not isinstance(title, str):
                raise ValueError(f"Invalid task title: must be a string, got {type(title).__name__}")
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty or contain only whitespace")
            update_data["title"] = title.strip()
        if description is not None:
            # Validate that description is a string before using it
            if not isinstance(description, str):
                raise ValueError(f"Invalid task description: must be a string, got {type(description).__name__}")
            update_data["description"] = description or ""

        try:
            # Call API to update the task
            response = self.api_client.update_task(task_id, **update_data)

            # Extract updated task data from response
            task_data = response.get("task", response)  # API might return task in a nested object

            if task_data:
                task = Task(
                    task_id=task_data.get("id"),
                    title=task_data.get("title", ""),
                    description=task_data.get("description", ""),
                    completed=task_data.get("completed", False)
                )
                return task
            return None
        except Exception as e:
            logging.error(f"Error updating task with ID {task_id}: {e}")
            raise ValueError(f"Failed to update task with ID {task_id}: {e}")

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID via API.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if it didn't exist
        """
        self.ensure_authenticated()

        try:
            response = self.api_client.delete_task(task_id)
            # Check if the deletion was successful based on the response
            return response.get("success", True)
        except Exception as e:
            logging.error(f"Error deleting task with ID {task_id}: {e}")
            raise ValueError(f"Failed to delete task with ID {task_id}: {e}")

    def toggle_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task by ID via API.

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            Task or None: The updated task if found, otherwise None
        """
        self.ensure_authenticated()

        try:
            response = self.api_client.toggle_task_completion(task_id)

            # Extract updated task data from response
            task_data = response.get("task", response)  # API might return task in a nested object

            if task_data:
                task = Task(
                    task_id=task_data.get("id"),
                    title=task_data.get("title", ""),
                    description=task_data.get("description", ""),
                    completed=task_data.get("completed", False)
                )
                return task
            return None
        except Exception as e:
            logging.error(f"Error toggling completion for task with ID {task_id}: {e}")
            raise ValueError(f"Failed to toggle completion for task with ID {task_id}: {e}")