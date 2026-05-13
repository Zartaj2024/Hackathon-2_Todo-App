import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Add phase_1/src to sys.path
phase1_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "phase_1"))
if phase1_path not in sys.path:
    sys.path.insert(0, phase1_path)

from src.services.task_service import TaskService
from src.models.task import Task

def test_task_service_create_task_mock():
    # Use skip_auth=True to use MockAPIClient
    service = TaskService(skip_auth=True)

    task = service.create_task("Test Task", "Test Description")

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert task.id == 1

def test_task_service_get_all_tasks_mock():
    service = TaskService(skip_auth=True)
    service.create_task("Task 1")
    service.create_task("Task 2")

    tasks = service.get_all_tasks()

    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"

def test_task_service_delete_task_mock():
    service = TaskService(skip_auth=True)
    task = service.create_task("To Delete")

    success = service.delete_task(task.id)
    assert success is True

    tasks = service.get_all_tasks()
    assert len(tasks) == 0

def test_task_service_toggle_completion_mock():
    service = TaskService(skip_auth=True)
    task = service.create_task("Toggle Me")

    updated_task = service.toggle_completion(task.id)
    assert updated_task.completed is True

    updated_task = service.toggle_completion(task.id)
    assert updated_task.completed is False
