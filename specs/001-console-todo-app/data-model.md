# Data Model: Console Todo Application

**Feature**: Console Todo Application
**Date**: 2026-01-20
**Status**: Complete

## Overview

This document defines the data models for the Console Todo Application based on the feature specification requirements.

## Entity: Task

### Attributes
- **id** (integer, required, unique, auto-generated)
  - Purpose: Unique identifier for each task
  - Constraints: Auto-incrementing integer, unique within the todo list
  - Validation: Must be positive integer, must be unique

- **title** (string, required, non-empty)
  - Purpose: Descriptive name of the task
  - Constraints: Cannot be empty or whitespace-only
  - Validation: Must be non-empty string after trimming whitespace

- **description** (string, optional)
  - Purpose: Additional details about the task
  - Constraints: Optional field, can be empty
  - Validation: Accepts any string including empty strings

- **completed** (boolean, required)
  - Purpose: Indicates whether the task is completed
  - Constraints: Must be boolean value
  - Default: False (as specified in FR-004)

### State Transitions
- `incomplete` → `completed`: When task completion is toggled and task was previously incomplete
- `completed` → `incomplete`: When task completion is toggled and task was previously completed

### Validation Rules
- Title must not be empty or contain only whitespace (FR-002, FR-010)
- ID must be unique within the todo list (FR-001)
- ID must be auto-generated (FR-001)

## Entity: TodoList

### Attributes
- **tasks** (list of Task objects, required)
  - Purpose: Collection of all tasks in the todo list
  - Constraints: Contains zero or more Task objects
  - Behavior: Maintains insertion order, allows duplicates only if they have different IDs

### Operations
- **add_task(task)**: Adds a new task to the list with auto-generated unique ID
- **get_all_tasks()**: Returns all tasks in the list
- **get_task_by_id(id)**: Returns the task with the specified ID or None if not found
- **update_task(id, updates)**: Updates the specified task with provided changes
- **delete_task(id)**: Removes the task with the specified ID
- **toggle_completion(id)**: Toggles the completion status of the specified task

### Validation Rules
- All operations must maintain uniqueness of task IDs
- Operations with invalid IDs must result in appropriate error handling (FR-009)
- Task list must persist in memory for the duration of the application session (FR-013)

## Relationships

- TodoList contains 0..N Task entities
- Each Task belongs to exactly one TodoList
- Task IDs are unique within their parent TodoList

## Error Conditions

- Attempting to access a task with non-existent ID should result in clear error message (FR-009)
- Attempting to add a task with empty title should result in validation error (FR-010)
- All error conditions must be handled gracefully without application crashes (FR-012)