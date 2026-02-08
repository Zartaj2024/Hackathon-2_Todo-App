# Data Model for Multi-User Todo Web Application

## Entity: User
**Description**: Represents an authenticated user of the system

**Fields**:
- `id`: String (Primary Key) - Unique identifier for the user
- `email`: String - User's email address (unique)
- `name`: String - User's display name
- `created_at`: DateTime - Timestamp when user account was created
- `updated_at`: DateTime - Timestamp when user account was last updated
- `is_active`: Boolean - Whether the account is active (default: true)

**Relationships**:
- One-to-Many: User has many Tasks (via user_id foreign key)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Name must not be empty
- ID must be unique and immutable

## Entity: Task
**Description**: Represents a task owned by a user

**Fields**:
- `id`: Integer (Primary Key) - Unique identifier for the task
- `title`: String - Task title (required, max 255 characters)
- `description`: String - Optional task description (nullable, max 1000 characters)
- `completed`: Boolean - Whether the task is completed (default: false)
- `user_id`: String (Foreign Key) - Reference to the owning user
- `created_at`: DateTime - Timestamp when task was created
- `updated_at`: DateTime - Timestamp when task was last updated

**Relationships**:
- Many-to-One: Task belongs to one User (via user_id foreign key)

**Validation Rules**:
- Title is required and cannot be empty or whitespace-only
- Title must be between 1 and 255 characters
- Description, if provided, must be between 1 and 1000 characters
- User_id must reference an existing user
- Completed status is boolean (true/false)
- Only the owning user can modify the task

## State Transitions

### Task State Transitions
- **Created**: When a new task is added by a user (completed = false initially)
- **Updated**: When task details (title, description) are modified by the owner
- **Completed**: When the completed status is changed to true by the owner
- **Reopened**: When the completed status is changed to false by the owner
- **Deleted**: When the task is removed by the owner

## Constraints
- Foreign key constraint: task.user_id must reference an existing user.id
- Task ownership: Only the user who owns a task can perform operations on it
- Data integrity: Prevent orphaned tasks without valid user references