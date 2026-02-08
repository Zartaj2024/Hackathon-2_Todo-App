"""
API client for connecting the CLI Todo App to the shared backend API.
"""

import requests
from typing import Optional, Dict, Any
import json
from urllib.parse import urljoin


class APIClient:
    """
    API client for communicating with the backend API.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the API client.

        Args:
            base_url: Base URL of the backend API
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.api_prefix = "/api/v1"

    def set_auth_token(self, token: str):
        """
        Set the authentication token for API requests.

        Args:
            token: JWT authentication token
        """
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

    def register_user(self, email: str, password: str, name: str) -> Dict[str, Any]:
        """
        Register a new user.

        Args:
            email: User's email address
            password: User's password
            name: User's name

        Returns:
            Dictionary containing registration response
        """
        url = urljoin(self.base_url, f"{self.api_prefix}/auth/register")
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Log in a user.

        Args:
            email: User's email address
            password: User's password

        Returns:
            Dictionary containing login response with token
        """
        url = urljoin(self.base_url, f"{self.api_prefix}/auth/login")
        payload = {
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    def get_tasks(self) -> Dict[str, Any]:
        """
        Get all tasks for the authenticated user.

        Returns:
            Dictionary containing tasks data
        """
        url = urljoin(self.base_url, f"{self.api_prefix}/tasks/")
        response = self.session.get(url)
        return self._handle_response(response)

    def create_task(self, title: str, description: str = "", completed: bool = False) -> Dict[str, Any]:
        """
        Create a new task for the authenticated user.

        Args:
            title: Task title
            description: Task description (optional)
            completed: Whether task is completed (default: False)

        Returns:
            Dictionary containing created task data
        """
        url = urljoin(self.base_url, f"{self.api_prefix}/tasks/")
        payload = {
            "title": title,
            "description": description,
            "completed": completed
        }
        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    def get_task(self, task_id: int) -> Dict[str, Any]:
        """
        Get a specific task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Dictionary containing task data
        """
        url = urljoin(self.base_url, f"{self.api_prefix}/tasks/{task_id}")
        response = self.session.get(url)
        return self._handle_response(response)

    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            Dictionary containing updated task data
        """
        url = urljoin(self.base_url, f"{self.api_prefix}/tasks/{task_id}")
        payload = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if completed is not None:
            payload["completed"] = completed

        response = self.session.put(url, json=payload)
        return self._handle_response(response)

    def toggle_task_completion(self, task_id: int) -> Dict[str, Any]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            Dictionary containing updated task data
        """
        url = urljoin(self.base_url, f"{self.api_prefix}/tasks/{task_id}/toggle-complete")
        response = self.session.patch(url)
        return self._handle_response(response)

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            Dictionary containing deletion response
        """
        url = urljoin(self.base_url, f"{self.api_prefix}/tasks/{task_id}")
        response = self.session.delete(url)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and return parsed JSON data.

        Args:
            response: requests.Response object

        Returns:
            Dictionary containing response data

        Raises:
            Exception: If the response indicates an error
        """
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {"error": "Invalid JSON response", "status_code": response.status_code}

        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}: {data}")

        return data