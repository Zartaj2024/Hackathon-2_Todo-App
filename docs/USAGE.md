# Todo Application Usage Guide

## Overview
This is a console-based todo application that allows users to manage their tasks through a simple menu-driven interface.

## Features
- Add new tasks with titles and optional descriptions
- View all tasks with their completion status
- Update existing tasks
- Delete tasks
- Toggle task completion status
- Robust error handling and validation

## How to Run
```bash
python src/main.py
```

## Menu Options
1. **Add a new task** - Create a new task with a title and optional description
2. **View all tasks** - Display all tasks with their ID, title, description, and completion status
3. **Update a task** - Modify an existing task's title or description
4. **Delete a task** - Remove a task by its ID
5. **Toggle task completion** - Switch a task between complete/incomplete status
6. **Exit** - Quit the application

## Error Handling
- Invalid task IDs are handled gracefully with clear error messages
- Empty or whitespace-only titles are rejected with validation errors
- Invalid menu selections prompt for retry
- The application never crashes due to user input errors

## Data Model
- **Task**: Each task has:
  - `id`: Unique numeric identifier (auto-generated)
  - `title`: Required string (cannot be empty)
  - `description`: Optional string
  - `completed`: Boolean indicating completion status (default: False)

## Limitations
- Data is stored in-memory only (lost when application exits)
- Single-user application
- No persistence between sessions