# Quickstart Guide: Console Todo Application

**Feature**: Console Todo Application
**Date**: 2026-01-20
**Status**: Complete

## Overview

This guide provides a quick overview of how to develop and run the Console Todo Application.

## Project Setup

### Prerequisites
- Python 3.13 or higher
- Basic understanding of Python programming

### Directory Structure
```
src/
├── main.py              # Main CLI entry point
├── models/
│   └── task.py          # Task entity and TodoList collection
├── services/
│   └── task_service.py  # Business logic for task operations
└── cli/
    └── cli_interface.py # CLI menu and user interaction handler

tests/
├── unit/
│   ├── test_task.py     # Unit tests for Task model
│   └── test_task_service.py # Unit tests for task service
├── integration/
│   └── test_cli_flow.py # Integration tests for CLI flows
└── contract/
    └── test_error_handling.py # Contract tests for error handling requirements
```

## Running the Application

### Direct Execution
```bash
python src/main.py
```

### Expected Behavior
1. Application starts with main menu
2. User can select operations: Add, View, Update, Delete, Toggle, Exit
3. All invalid inputs are handled gracefully with error messages
4. Application never crashes due to user input (per FR-012)

## Development Workflow

### 1. Implement Models
- Start with `models/task.py` - implement Task and TodoList classes
- Ensure all validation rules from data-model.md are enforced

### 2. Implement Services
- Develop `services/task_service.py` - implement business logic
- Include proper error handling for all operations

### 3. Implement CLI Interface
- Build `cli/cli_interface.py` - implement user interface
- Ensure all menu options are available and error recovery works

### 4. Testing
- Write unit tests for each component
- Verify all error handling scenarios work correctly
- Test all functional requirements from spec

## Key Features

### Add Task (FR-001, FR-002, FR-003, FR-004)
- Prompts for title (required) and description (optional)
- Auto-generates unique ID
- Sets completion status to false by default

### View Tasks (FR-005)
- Displays all tasks with ID, title, description, and completion status
- Shows completion status clearly

### Update Task (FR-006)
- Allows modifying title and description by task ID
- Validates title is not empty

### Delete Task (FR-007)
- Removes task by ID
- Handles invalid IDs gracefully

### Toggle Completion (FR-008)
- Switches completion status of task by ID
- Handles invalid IDs gracefully

### Error Handling (FR-009, FR-010, FR-011, FR-012)
- Validates all inputs
- Provides clear error messages
- Never crashes on invalid input
- Returns to main menu after errors

## Testing Commands

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test Categories
```bash
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/contract/      # Contract tests
```

## Success Criteria Verification

Verify the following success criteria are met:
- SC-001: Users can add, view, update, delete, and toggle without crashes
- SC-002: All error conditions handled with clear messages
- SC-003: Responsive under 1 second per operation
- SC-004: 100% of invalid inputs result in proper error messages
- SC-005: Operations completed with no more than 3 prompts
- SC-006: Task data remains consistent during session