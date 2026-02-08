# AI Chatbot API Documentation

This document provides comprehensive API documentation for the AI chatbot endpoints.

## Chat Endpoint

### POST `/api/v1/users/{user_id}/chat`

Process a conversation with the AI chatbot.

#### Parameters
- `user_id` (path, string, required): The ID of the authenticated user

#### Request Body
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Add a task to buy groceries",
      "timestamp": "2023-12-01T10:00:00Z"
    }
  ]
}
```

**Request Body Properties:**
- `messages` (array, required): Array of messages in the conversation
  - `role` (string, required): Either "user" or "assistant"
  - `content` (string, required): The message content
  - `timestamp` (string, optional): ISO 8601 timestamp

#### Responses

**200 Success:**
```json
{
  "messages": [
    {
      "role": "assistant",
      "content": "Task 'buy groceries' added successfully",
      "timestamp": "2023-12-01T10:00:05Z"
    }
  ],
  "conversation_id": "uuid-string"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication required. Please log in to continue."
}
```

**403 Forbidden:**
```json
{
  "detail": "Access denied. You don't have permission to perform this action."
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "messages"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "An unexpected error occurred. Our team has been notified."
}
```

## Conversation Endpoints

### GET `/api/v1/users/{user_id}/chat/conversations`

Retrieve all conversations for a user.

#### Parameters
- `user_id` (path, string, required): The ID of the authenticated user

#### Responses

**200 Success:**
```json
[
  {
    "id": "uuid-string",
    "user_id": "user-uuid",
    "title": "Task management discussion",
    "is_active": true,
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T10:00:00Z"
  }
]
```

### GET `/api/v1/users/{user_id}/chat/conversation/{conversation_id}`

Retrieve a specific conversation with its messages.

#### Parameters
- `user_id` (path, string, required): The ID of the authenticated user
- `conversation_id` (path, string, required): The ID of the conversation

#### Responses

**200 Success:**
```json
{
  "conversation": {
    "id": "uuid-string",
    "user_id": "user-uuid",
    "title": "Task management discussion",
    "is_active": true,
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T10:00:00Z"
  },
  "messages": [
    {
      "id": "uuid-string",
      "conversation_id": "conversation-uuid",
      "role": "user",
      "content": "Add a task to buy groceries",
      "timestamp": "2023-12-01T10:00:00Z",
      "message_type": "text",
      "metadata_json": null
    }
  ]
}
```

### GET `/api/v1/users/{user_id}/chat/token`

Generate a token for chat authentication (if needed).

#### Parameters
- `user_id` (path, string, required): The ID of the authenticated user

#### Responses

**200 Success:**
```json
{
  "success": true,
  "message": "Token generation endpoint - would return token in real implementation"
}
```

## Error Codes

The API uses the following HTTP status codes:

- `200`: Success
- `400`: Bad Request - Request body or parameters are invalid
- `401`: Unauthorized - Authentication token is missing or invalid
- `403`: Forbidden - User doesn't have permission for this action
- `404`: Not Found - Requested resource doesn't exist
- `422`: Unprocessable Entity - Validation errors in request body
- `429`: Too Many Requests - Rate limit exceeded
- `500`: Internal Server Error - Unexpected server error
- `502`: Bad Gateway - External service (like OpenAI) unavailable
- `503`: Service Unavailable - System overloaded

## Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

The user ID in the path must match the user ID in the authenticated token, otherwise a 403 Forbidden error will be returned.