"""
Main entry point for the Todo Console Application.

This module initializes the application and runs the CLI interface.
"""

from src.services.task_service import TaskService
from src.cli.cli_interface import CLIInterface


def main():
    """
    Main function to initialize and run the Todo Application.

    Creates the necessary services and starts the CLI interface.
    """
    # Initialize the task service with the API base URL
    # By default, the backend runs on port 8000
    task_service = TaskService(api_base_url="http://localhost:8000")

    # Initialize the CLI interface with the task service
    cli_interface = CLIInterface(task_service)

    # Run the CLI interface
    try:
        cli_interface.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Thank you for using the Todo Application. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Exiting the application.")


if __name__ == "__main__":
    main()