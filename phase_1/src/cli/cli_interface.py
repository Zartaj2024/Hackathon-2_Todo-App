"""
CLI interface for the Todo Console Application.

This module implements the command-line interface that allows users
to interact with the task management system via the shared API.
"""

from typing import Optional
import sys
from src.services.task_service import TaskService


class CLIInterface:
    """
    Command-line interface for interacting with the task management system.

    Provides a menu-driven interface for users to perform all task operations.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the CLI interface with a task service.

        Args:
            task_service (TaskService): The service to handle task operations
        """
        self.task_service = task_service
        self.authenticated = False

    def display_main_menu(self) -> None:
        """Display the main menu options to the user."""
        print("\n" + "="*40)
        print("TODO APPLICATION")
        print("="*40)

        if not self.authenticated:
            print("NOT AUTHENTICATED - Please log in or register first")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
        else:
            print(f"Logged in as: {getattr(self.task_service, '_current_user_email', 'Unknown')}")
            print("1. Add a new task")
            print("2. View all tasks")
            print("3. Update a task")
            print("4. Delete a task")
            print("5. Toggle task completion")
            print("6. Logout")
            print("7. Exit")
        print("-"*40)

    def authenticate_user(self) -> bool:
        """
        Handle user authentication process.

        Returns:
            bool: True if authentication successful, False otherwise
        """
        print("\n--- AUTHENTICATION ---")
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()

        if not email or not password:
            print("Email and password are required.")
            return False

        try:
            if self.task_service.authenticate(email, password):
                print("Login successful!")
                self.authenticated = True
                setattr(self.task_service, '_current_user_email', email)
                return True
            else:
                print("Login failed. Invalid credentials or server error.")
                return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def register_user(self) -> bool:
        """
        Handle user registration process.

        Returns:
            bool: True if registration successful, False otherwise
        """
        print("\n--- REGISTRATION ---")
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()
        name = input("Enter your name: ").strip()

        if not email or not password or not name:
            print("Email, password, and name are required.")
            return False

        try:
            if self.task_service.register_and_authenticate(email, password, name):
                print("Registration and login successful!")
                self.authenticated = True
                setattr(self.task_service, '_current_user_email', email)
                return True
            else:
                print("Registration failed. Please try again.")
                return False
        except Exception as e:
            print(f"Registration error: {e}")
            return False

    def get_user_choice(self) -> int:
        """
        Get and validate the user's menu choice.

        Returns:
            int: The user's choice (depends on auth status), or -1 if invalid input
        """
        max_choice = 7 if self.authenticated else 3
        try:
            choice = int(input(f"Enter your choice (1-{max_choice}): "))
            if 1 <= choice <= max_choice:
                return choice
            else:
                print(f"Invalid choice. Please enter a number between 1 and {max_choice}.")
                return -1
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {max_choice}.")
            return -1

    def add_task(self) -> None:
        """Handle adding a new task via user input."""
        if not self.authenticated and not getattr(self.task_service, 'skip_auth', False):
            print("Error: You must be logged in to add tasks.")
            return

        print("\n--- Add New Task ---")

        title = input("Enter task title: ").strip()
        if not title:
            print("Error: Task title cannot be empty.")
            return

        description = input("Enter task description (optional, press Enter to skip): ").strip()
        if not description:
            description = None

        try:
            task = self.task_service.create_task(title, description)
            print(f"Task '{task.title}' added successfully with ID {task.id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def view_all_tasks(self) -> None:
        """Display all tasks to the user."""
        if not self.authenticated and not getattr(self.task_service, 'skip_auth', False):
            print("Error: You must be logged in to view tasks.")
            return

        print("\n--- All Tasks ---")
        try:
            tasks = self.task_service.get_all_tasks()

            if not tasks:
                print("No tasks found.")
            else:
                for task in tasks:
                    print(task)
        except Exception as e:
            print(f"Error retrieving tasks: {e}")

    def update_task(self) -> None:
        """Handle updating an existing task via user input."""
        if not self.authenticated and not getattr(self.task_service, 'skip_auth', False):
            print("Error: You must be logged in to update tasks.")
            return

        print("\n--- Update Task ---")

        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        try:
            existing_task = self.task_service.get_task_by_id(task_id)
            if existing_task is None:
                print(f"No task found with ID {task_id}.")
                return
        except Exception as e:
            print(f"Error retrieving task: {e}")
            return

        print(f"Current task: {existing_task}")

        new_title = input(f"Enter new title (current: '{existing_task.title}', press Enter to keep current): ").strip()
        new_description = input(f"Enter new description (current: '{existing_task.description}', press Enter to keep current): ").strip()

        # Prepare updates
        title = new_title if new_title else existing_task.title
        description = new_description if new_description else existing_task.description

        # If description was explicitly set to empty string, use None
        if new_description == "":
            description = None

        try:
            updated_task = self.task_service.update_task(task_id, title, description)
            if updated_task:
                print(f"Task with ID {task_id} updated successfully.")
            else:
                print(f"Failed to update task with ID {task_id}.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error updating task: {e}")

    def delete_task(self) -> None:
        """Handle deleting a task via user input."""
        if not self.authenticated and not getattr(self.task_service, 'skip_auth', False):
            print("Error: You must be logged in to delete tasks.")
            return

        print("\n--- Delete Task ---")

        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        try:
            success = self.task_service.delete_task(task_id)
            if success:
                print(f"Task with ID {task_id} deleted successfully.")
            else:
                print(f"No task found with ID {task_id}.")
        except Exception as e:
            print(f"Error deleting task: {e}")

    def toggle_completion(self) -> None:
        """Handle toggling a task's completion status via user input."""
        if not self.authenticated and not getattr(self.task_service, 'skip_auth', False):
            print("Error: You must be logged in to toggle task completion.")
            return

        print("\n--- Toggle Task Completion ---")

        try:
            task_id = int(input("Enter task ID to toggle: "))
        except ValueError:
            print("Invalid task ID. Please enter a number.")
            return

        try:
            task = self.task_service.toggle_completion(task_id)
            if task:
                status = "completed" if task.completed else "incomplete"
                print(f"Task with ID {task_id} marked as {status}.")
            else:
                print(f"No task found with ID {task_id}.")
        except Exception as e:
            print(f"Error toggling task completion: {e}")

    def logout(self) -> None:
        """Handle user logout."""
        self.authenticated = False
        self.task_service.auth_token = None
        # Reset session in API client
        self.task_service.api_client.session = __import__('requests').Session()
        print("Logged out successfully.")

    def run(self) -> None:
        """
        Run the main CLI loop continuously until the user chooses to exit.

        Handles all user interactions and routes to appropriate methods.
        """
        print("Welcome to the Todo Application!")
        print("Connect to your account to manage tasks across both CLI and web apps.")

        while True:
            self.display_main_menu()
            choice = self.get_user_choice()

            if choice == -1:
                # Invalid input, continue the loop
                continue
            elif not self.authenticated:
                # Handle unauthenticated menu choices
                if choice == 1:
                    self.register_user()
                elif choice == 2:
                    self.authenticate_user()
                elif choice == 3:
                    print("Thank you for using the Todo Application. Goodbye!")
                    sys.exit(0)
            else:
                # Handle authenticated menu choices
                if choice == 1:
                    self.add_task()
                elif choice == 2:
                    self.view_all_tasks()
                elif choice == 3:
                    self.update_task()
                elif choice == 4:
                    self.delete_task()
                elif choice == 5:
                    self.toggle_completion()
                elif choice == 6:
                    self.logout()
                elif choice == 7:
                    print("Thank you for using the Todo Application. Goodbye!")
                    sys.exit(0)
                else:
                    # This shouldn't happen due to validation, but just in case
                    print("Unexpected choice. Please try again.")