# AI-Powered Chatbot - Implementation Plan

## 1. Overall System Architecture

```
┌─────────────────┐    HTTP/SSE     ┌──────────────────────┐
│   Frontend      │◄────────────────►│   Backend/FastAPI    │
│   (/chat page)  │                 │                      │
└─────────┬───────┘                 │ ┌─────────────────┐  │
          │                         │ │  OpenAI Agent   │  │
          │                         │ │  SDK            │  │
          │                         │ └─────────┬───────┘  │
          │                         │           │          │
          │                         │   ┌───────▼────────┐ │
          │                         │   │ MCP Tools      │ │
          │                         │   │ (add_task,     │ │
          │                         │   │  list_tasks,   │ │
          │                         │   │  etc.)         │ │
          │                         │   └─────────┬──────┘ │
          │                         │             │        │
          │                         │    ┌────────▼────────┐│
          │                         │    │ Task Services   ││
          │                         │    │ (reuse existing)││
          │                         │    └────────┬────────┘│
          │                         │             │         │
          │                         │    ┌────────▼────────┐│
          │                         │    │ Database        ││
          │                         │    │ (PostgreSQL)    ││
          │                         │    └─────────────────┘│
          │                         └──────────────────────┘
          │
          │
          ▼
   Browser/Client
```

## 2. Backend Components

### 2.1 New FastAPI Endpoint: POST /api/{user_id}/chat

```python
@router.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user_from_jwt)
):
    """
    Main chat endpoint that integrates with OpenAI Agent SDK
    Validates user authentication and routes to AI agent
    """
    # Verify user_id matches authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Create conversation context
    conversation_context = {
        "user_id": user_id,
        "messages": chat_request.messages
    }

    # Pass to OpenAI Agent for processing
    agent_response = await process_with_openai_agent(conversation_context)

    return ChatResponse(messages=agent_response)
```

### 2.2 OpenAI Agent SDK Integration

- Define agent with system instructions for task management
- Configure tools for CRUD operations on tasks
- Implement context passing for user-specific operations
- Handle conversation history and state management

### 2.3 MCP Server Setup

- Run MCP server on port 8001 (separate from main API)
- Register 5 specific tools as endpoints
- Implement stateless execution model
- Ensure proper authentication forwarding

### 2.4 Reuse of Existing Task Services

- Leverage existing task CRUD logic in services/
- Adapt for AI agent consumption
- Maintain consistent error handling
- Preserve existing validation layers

### 2.5 Conversation & Message Persistence

- Create Conversation model to track chat sessions
- Create Message model to store chat history
- Implement service layer for conversation management
- Add indexes for efficient retrieval

## 3. MCP Tools Specification

### 3.1 add_task Tool
```json
{
  "name": "add_task",
  "description": "Add a new task for the user",
  "input_schema": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "description": "Task title"},
      "description": {"type": "string", "description": "Task description (optional)"},
      "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"},
      "due_date": {"type": "string", "format": "date", "description": "Due date in YYYY-MM-DD format (optional)"}
    },
    "required": ["title"]
  }
}
```

### 3.2 list_tasks Tool
```json
{
  "name": "list_tasks",
  "description": "List all tasks for the user",
  "input_schema": {
    "type": "object",
    "properties": {
      "status": {"type": "string", "enum": ["all", "completed", "pending"], "default": "all"},
      "limit": {"type": "integer", "default": 10}
    }
  }
}
```

### 3.3 complete_task Tool
```json
{
  "name": "complete_task",
  "description": "Mark a task as completed",
  "input_schema": {
    "type": "object",
    "properties": {
      "task_id": {"type": "integer", "description": "ID of the task to complete"}
    },
    "required": ["task_id"]
  }
}
```

### 3.4 update_task Tool
```json
{
  "name": "update_task",
  "description": "Update an existing task",
  "input_schema": {
    "type": "object",
    "properties": {
      "task_id": {"type": "integer", "description": "ID of the task to update"},
      "title": {"type": "string", "description": "New task title (optional)"},
      "description": {"type": "string", "description": "New task description (optional)"},
      "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "New priority (optional)"},
      "due_date": {"type": "string", "format": "date", "description": "New due date (optional)"}
    },
    "required": ["task_id"]
  }
}
```

### 3.5 delete_task Tool
```json
{
  "name": "delete_task",
  "description": "Delete a task",
  "input_schema": {
    "type": "object",
    "properties": {
      "task_id": {"type": "integer", "description": "ID of the task to delete"}
    },
    "required": ["task_id"]
  }
}
```

## 4. Authentication & Security Flow

- Verify JWT token from incoming request
- Extract user_id from token claims
- Ensure user_id matches the path parameter
- Pass user context to MCP tools
- Implement role-based access (users can only access their own tasks)

## 5. Frontend Integration

### 5.1 New Page: /chat
- Dedicated chat interface at /chat
- Real-time message display
- Text input with send functionality
- Loading states for AI responses

### 5.2 OpenAI ChatKit Embedding
- If available, use ChatKit components
- Fallback to custom chat UI if ChatKit is unavailable
- Token generation endpoint for ChatKit authentication (if needed)

### 5.3 Fallback Simple Chat UI
- Basic message bubbles
- Text input field
- Send button
- Auto-scroll to new messages

## 6. Error Handling Strategy

- Tool-level errors with consistent format
- Agent-level fallback messages
- HTTP error codes for the chat endpoint
- Rate limiting to prevent abuse

## 7. Database Schema Changes

- Add Conversation table
- Add Message table
- Indexes for efficient querying
- Foreign key relationships to users

## 8. Testing Approach

- Unit tests for MCP tools
- Integration tests for chat flow
- Mock OpenAI Agent for testing
- End-to-end tests for complete user journey

## 9. Deployment Considerations

- MCP server deployment alongside main API
- Environment-specific configurations
- Scaling considerations for AI requests
- Monitoring and logging for AI interactions