# AI Chatbot Quickstart Guide

This guide will help you get started with testing the AI-powered chatbot feature.

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL database
- Hugging Face account with API key
- The Todo App backend and frontend services running

## Setup

1. Get your Hugging Face API key from your Hugging Face account, then add it to your `.env` file:
   ```
   HF_API_KEY=your-huggingface-api-key-here
   ```

2. Make sure the MCP server is running on port 8001:
   ```bash
   cd backend
   python -m mcp_server.server
   ```

3. Start the main backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

4. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

## Testing the Chatbot

### 1. Access the Chat Interface
- Navigate to `/chat` in your browser
- Log in with your credentials
- You should see the chat interface with a message from the AI assistant

### 2. Test Basic Commands
Try these commands to verify functionality:

**Adding a task:**
- "Add a task to buy groceries"
- "Create a task to call mom tomorrow"
- "Add a high priority task to prepare presentation"

**Listing tasks:**
- "Show my tasks"
- "What tasks do I have?"
- "List all my tasks"

**Updating tasks:**
- "Update task 1 to 'buy organic groceries'"
- "Change task 2 priority to high"

**Completing tasks:**
- "Complete task 1"
- "Mark task 2 as done"
- "Finish task 3"

**Deleting tasks:**
- "Delete task 1"
- "Remove task 2"

### 3. Verify Database Operations
- Check that conversations are stored in the `conversations` table
- Check that messages are stored in the `messages` table
- Verify that tasks are properly created/updated/deleted in the `tasks` table with `ai_processed` flag set to `true`

### 4. Test Error Scenarios
- Try referencing a non-existent task ID
- Attempt operations without authentication
- Submit malformed commands to test error handling

## Troubleshooting

### Common Issues

1. **OpenAI API Error**: Ensure your API key is valid and has sufficient credits
2. **MCP Server Not Responding**: Verify the MCP server is running on port 8001
3. **Database Connection Issues**: Check your database connection settings
4. **Authentication Errors**: Ensure you're logged in and JWT tokens are valid

### Logs to Check

- Backend logs for API and database operations
- MCP server logs for tool execution
- Frontend console for client-side errors

## Best Practices

- Always test with realistic user scenarios
- Verify data integrity in the database after operations
- Test both happy path and error scenarios
- Check that user isolation is maintained (users can only access their own data)