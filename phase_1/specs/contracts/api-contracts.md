# API Contracts: Phase 1 Execution Plan for Python Console Application

**Feature**: Phase 1 Execution Plan for Python Console Application
**Date**: 2026-01-20
**Status**: Complete

## Overview

This document defines the API contracts for the Phase 1 Execution Plan for Python Console Application based on the functional requirements.

## Core Operations

### 1. Add Task
- **Method**: `task_service.create_task(title, description)`
- **Parameters**:
  - `title` (string, required): Task title (non-empty)
  - `description` (string, optional): Task description
- **Returns**: `Task` object with auto-generated ID and completed=False
- **Errors**:
  - ValidationError if title is empty
  - Returns appropriate error message for user

### 2. View All Tasks
- **Method**: `task_service.get_all_tasks()`
- **Parameters**: None
- **Returns**: List of all `Task` objects
- **Errors**: None (returns empty list if no tasks)

### 3. Get Task by ID
- **Method**: `task_service.get_task_by_id(task_id)`
- **Parameters**:
  - `task_id` (integer, required): Unique identifier of task
- **Returns**: `Task` object or None if not found
- **Errors**: Returns appropriate error message for invalid IDs

### 4. Update Task
- **Method**: `task_service.update_task(task_id, updates)`
- **Parameters**:
  - `task_id` (integer, required): Unique identifier of task
  - `updates` (dict): Fields to update (title, description)
- **Returns**: Updated `Task` object or None if not found
- **Errors**:
  - ValidationError if title is empty
  - Returns appropriate error message for invalid IDs

### 5. Delete Task
- **Method**: `task_service.delete_task(task_id)`
- **Parameters**:
  - `task_id` (integer, required): Unique identifier of task
- **Returns**: Boolean indicating success
- **Errors**: Returns appropriate error message for invalid IDs

### 6. Toggle Task Completion
- **Method**: `task_service.toggle_completion(task_id)`
- **Parameters**:
  - `task_id` (integer, required): Unique identifier of task
- **Returns**: Updated `Task` object or None if not found
- **Errors**: Returns appropriate error message for invalid IDs

## CLI Interface Contracts

### Main Menu Loop
- **Method**: `cli_interface.run()`
- **Behavior**: Continuously presents menu options and handles user selection
- **Valid Options**:
  - 1: Add Task
  - 2: View All Tasks
  - 3: Update Task
  - 4: Delete Task
  - 5: Toggle Task Completion
  - 6: Exit
- **Error Handling**: Invalid input results in retry prompt (FR-010)

### Input Validation
- **Contract**: All user inputs must be validated before processing
- **Requirements**:
  - Empty titles rejected with validation error (FR-008)
  - Invalid task IDs handled with clear error messages (FR-009)
  - Non-numeric inputs handled gracefully

## Error Handling Contracts

### General Error Handling
- **Requirement**: No operation should cause application crash (FR-012)
- **Pattern**: All operations wrapped in try-catch blocks
- **Response**: Clear error messages returned to user
- **Recovery**: Application returns to main menu after error

### Validation Error Contract
- **Trigger**: Invalid input provided (empty title, invalid ID)
- **Response**: Clear error message displayed to user
- **State**: Application remains in usable state
- **Retry**: User prompted to try again or return to main menu

### System Error Contract
- **Trigger**: Unexpected error occurs during operation
- **Response**: Safe error message displayed (no internal details leaked)
- **State**: Application returns to stable state
- **Logging**: Error details logged internally for debugging