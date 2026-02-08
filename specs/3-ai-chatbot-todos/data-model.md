# AI-Powered Chatbot - Data Model

## 1. Conversation Model

### Conversation
- **id**: UUID (Primary Key)
- **user_id**: UUID (Foreign Key to Users table)
- **created_at**: DateTime (Timestamp of creation)
- **updated_at**: DateTime (Timestamp of last update)
- **title**: String (Optional, auto-generated from first message)
- **is_active**: Boolean (Whether conversation is ongoing)

**Relationships**:
- One Conversation has many Messages
- Many Messages belong to one Conversation
- One Conversation belongs to one User
- One User has many Conversations

**Indexes**:
- idx_conversations_user_id (user_id) - for efficient user lookup
- idx_conversations_created_at (created_at DESC) - for chronological ordering
- idx_conversations_active (is_active) - for active conversation filtering

## 2. Message Model

### Message
- **id**: UUID (Primary Key)
- **conversation_id**: UUID (Foreign Key to Conversations table)
- **role**: String (Either "user" or "assistant")
- **content**: Text (The actual message content)
- **timestamp**: DateTime (When the message was sent)
- **message_type**: String (Either "text", "command", "response", "error")
- **metadata**: JSONB (Additional data like tool calls, parameters)

**Relationships**:
- Many Messages belong to one Conversation
- One Conversation has many Messages

**Indexes**:
- idx_messages_conversation_id (conversation_id) - for conversation lookup
- idx_messages_timestamp (timestamp ASC) - for chronological ordering
- idx_messages_role (role) - for filtering by sender type

## 3. Task Model (Extended)

### Task (Existing model with extensions for AI integration)
- **id**: Integer (Primary Key)
- **user_id**: UUID (Foreign Key to Users table) - EXISTING
- **title**: String - EXISTING
- **description**: String (Optional) - EXISTING
- **completed**: Boolean (Default: false) - EXISTING
- **created_at**: DateTime - EXISTING
- **updated_at**: DateTime - EXISTING
- **priority**: String (Enum: low, medium, high; Default: medium) - EXISTING
- **due_date**: Date (Optional) - EXISTING
- **ai_processed**: Boolean (Whether this task was created via AI, Default: false)

**Indexes**:
- idx_tasks_user_id (user_id) - for user-specific queries
- idx_tasks_completed (completed) - for filtering completed tasks
- idx_tasks_priority (priority) - for priority-based sorting
- idx_tasks_due_date (due_date) - for due date filtering

## 4. Validation Rules

### Conversation Validation
- user_id must exist in Users table
- created_at and updated_at are automatically set
- title is optional, defaults to first few words of first message
- is_active defaults to true when created

### Message Validation
- conversation_id must exist in Conversations table
- role must be either "user" or "assistant"
- content cannot be empty
- timestamp is automatically set to current time
- message_type must be one of: "text", "command", "response", "error"
- metadata is optional JSON object

### Task Validation (Extended)
- user_id must exist in Users table
- title is required and must be 1-255 characters
- priority must be one of: "low", "medium", "high"
- due_date must be a future date if provided
- ai_processed is set to true when task is created via AI chat

## 5. State Transitions

### Conversation States
- **Active**: When created or when user sends a message
- **Inactive**: After period of inactivity (configurable, e.g., 24 hours)

### Task State Transitions
- **Created**: When task is first added (via AI or manual)
- **Updated**: When task details are modified
- **Completed**: When task is marked as done
- **Deleted**: When task is removed

## 6. Relationships and Constraints

### Foreign Key Constraints
- conversations.user_id → users.id (CASCADE DELETE)
- messages.conversation_id → conversations.id (CASCADE DELETE)
- tasks.user_id → users.id (CASCADE DELETE)

### Unique Constraints
- None for conversations (multiple per user allowed)
- None for messages (multiple per conversation allowed)
- Standard primary key uniqueness for all tables

## 7. Additional Considerations

### Performance Optimization
- Partition Messages table by conversation_id if needed for large datasets
- Regular cleanup job for inactive conversations (optional)
- Caching strategy for frequently accessed conversation histories

### Security Considerations
- All foreign key relationships enforce referential integrity
- User data isolation through user_id scoping
- No direct cross-user access to conversations or messages

### Audit Trail
- created_at and updated_at timestamps on all tables
- message_type field to distinguish between different message kinds
- metadata field for storing additional context about AI interactions