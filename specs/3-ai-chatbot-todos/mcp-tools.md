# AI-Powered Chatbot - MCP Tools Specification

## 1. Overview

This document defines the 5 MCP (Multi-Component Protocol) tools that will be integrated with the OpenAI Agent SDK for handling natural language task management commands. Each tool corresponds to a specific CRUD operation for tasks.

## 2. Common Tool Structure

All tools follow the same basic structure:
- Name: Unique identifier for the tool
- Description: Human-readable description of the tool's purpose
- Parameters: JSON Schema defining expected input
- Return Format: Consistent error and success responses

## 3. Tool Specifications

### 3.1 add_task Tool

**Name**: `add_task`

**Description**: Creates a new task for the authenticated user based on natural language input.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Title of the task to be created",
      "minLength": 1,
      "maxLength": 255
    },
    "description": {
      "type": "string",
      "description": "Detailed description of the task (optional)",
      "maxLength": 1000
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "Priority level of the task (optional, defaults to medium)",
      "default": "medium"
    },
    "due_date": {
      "type": "string",
      "format": "date",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
      "description": "Due date in YYYY-MM-DD format (optional)"
    }
  },
  "required": ["title"]
}
```

**Input Validation**:
- Title must be 1-255 characters
- Description (if provided) must be ≤1000 characters
- Priority must be one of: "low", "medium", "high"
- Due date must be in YYYY-MM-DD format if provided

**Success Response**:
```json
{
  "success": true,
  "task_id": 123,
  "message": "Task 'Buy groceries' added successfully"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Invalid input: title is required and must be between 1-255 characters"
}
```

### 3.2 list_tasks Tool

**Name**: `list_tasks`

**Description**: Retrieves a list of tasks for the authenticated user with optional filtering.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["all", "completed", "pending"],
      "description": "Filter tasks by completion status (optional, defaults to all)",
      "default": "all"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "description": "Maximum number of tasks to return (optional, defaults to 10)",
      "default": 10
    },
    "offset": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of tasks to skip (for pagination, optional)",
      "default": 0
    }
  }
}
```

**Input Validation**:
- Status must be one of: "all", "completed", "pending"
- Limit must be between 1-100
- Offset must be ≥0

**Success Response**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "priority": "medium",
      "due_date": "2023-12-31",
      "created_at": "2023-12-01T10:00:00Z"
    }
  ],
  "total_count": 1,
  "message": "Successfully retrieved 1 task(s)"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Invalid input: status must be one of 'all', 'completed', 'pending'"
}
```

### 3.3 complete_task Tool

**Name**: `complete_task`

**Description**: Marks a specific task as completed for the authenticated user.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "minimum": 1,
      "description": "ID of the task to mark as completed"
    }
  },
  "required": ["task_id"]
}
```

**Input Validation**:
- Task ID must be a positive integer
- Task must exist and belong to the authenticated user

**Success Response**:
```json
{
  "success": true,
  "task_id": 1,
  "message": "Task 'Buy groceries' marked as completed"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Task with ID 1 not found or you don't have permission to modify it"
}
```

### 3.4 update_task Tool

**Name**: `update_task`

**Description**: Updates an existing task with new information for the authenticated user.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "minimum": 1,
      "description": "ID of the task to update"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "description": "New title for the task (optional)"
    },
    "description": {
      "type": "string",
      "maxLength": 1000,
      "description": "New description for the task (optional)"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "New priority level (optional)"
    },
    "due_date": {
      "type": "string",
      "format": "date",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
      "description": "New due date in YYYY-MM-DD format (optional)"
    },
    "completed": {
      "type": "boolean",
      "description": "Whether the task is completed (optional)"
    }
  },
  "required": ["task_id"]
}
```

**Input Validation**:
- Task ID must be a positive integer
- If provided, title must be 1-255 characters
- If provided, description must be ≤1000 characters
- If provided, priority must be one of: "low", "medium", "high"
- If provided, due date must be in YYYY-MM-DD format
- If provided, completed must be a boolean value
- Task must exist and belong to the authenticated user

**Success Response**:
```json
{
  "success": true,
  "task_id": 1,
  "updated_fields": ["title", "priority"],
  "message": "Task 'Buy groceries' updated successfully"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Task with ID 1 not found or you don't have permission to modify it"
}
```

### 3.5 delete_task Tool

**Name**: `delete_task`

**Description**: Removes a task from the authenticated user's task list.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "minimum": 1,
      "description": "ID of the task to delete"
    }
  },
  "required": ["task_id"]
}
```

**Input Validation**:
- Task ID must be a positive integer
- Task must exist and belong to the authenticated user

**Success Response**:
```json
{
  "success": true,
  "task_id": 1,
  "message": "Task 'Buy groceries' deleted successfully"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Task with ID 1 not found or you don't have permission to delete it"
}
```

## 4. Common Error Patterns

### Authentication Errors
```json
{
  "success": false,
  "error": "Authentication failed: Invalid user token"
}
```

### Authorization Errors
```json
{
  "success": false,
  "error": "Authorization failed: You don't have permission to access this resource"
}
```

### Validation Errors
```json
{
  "success": false,
  "error": "Validation failed: {specific validation error}"
}
```

### Internal Errors
```json
{
  "success": false,
  "error": "Internal server error: Please try again later"
}
```

## 5. MCP Server Implementation

### Server Configuration
- **Port**: 8001 (separate from main API server)
- **Endpoint Pattern**: `/tools/{tool_name}`
- **Request Format**: POST with JSON body containing parameters
- **Response Format**: JSON with consistent success/error structure

### Tool Registration
```python
# Example registration pattern
MCP_TOOLS = {
    "add_task": add_task_handler,
    "list_tasks": list_tasks_handler,
    "complete_task": complete_task_handler,
    "update_task": update_task_handler,
    "delete_task": delete_task_handler
}
```

### Security Implementation
- Validate user authentication for each tool call
- Verify user ownership of tasks before operations
- Implement rate limiting per user
- Log all tool invocations for audit purposes

## 6. Integration with OpenAI Agent SDK

### Tool Definitions for Agent
```python
openai_tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Creates a new task for the user",
            "parameters": { /* add_task parameters */ }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Lists tasks for the user",
            "parameters": { /* list_tasks parameters */ }
        }
    },
    // ... other tools
]
```

This specification ensures consistent behavior across all tools while providing clear error reporting and validation for the AI agent integration.