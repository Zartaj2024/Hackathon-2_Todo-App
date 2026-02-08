# Multi-User Todo Web Application

A full-stack web application that allows multiple users to manage their personal tasks with secure authentication and proper task ownership enforcement.

## Features

- User registration and authentication with JWT tokens
- Create, read, update, and delete personal tasks
- Mark tasks as complete/incomplete
- Secure task ownership (users can only see and modify their own tasks)
- Responsive web interface
- AI-Powered Chatbot for natural language task management

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI (Python) with SQLModel ORM
- **Database**: PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **AI Integration**: OpenAI Agent SDK with MCP tools
- **AI Chatbot**: Natural language processing for task management

## AI-Powered Chatbot Feature

The application includes an advanced AI-powered chatbot that allows users to manage their tasks using natural language commands. The chatbot leverages OpenAI's GPT models and MCP (Multi-Component Protocol) tools to perform task management operations.

### Chatbot Capabilities
- Natural language task management (add, list, update, complete, delete tasks)
- Conversational interface for task management
- Secure user authentication and authorization
- Conversation history tracking
- Real-time messaging interface
- Support for multiple AI providers (Google Gemini, Hugging Face)

### How to Use the Chatbot
1. Navigate to the `/chat` page in the application
2. Use natural language commands such as:
   - "Add a task to buy groceries"
   - "Show my tasks"
   - "Complete task 1"
   - "Update task 2 to 'buy organic groceries'"
   - "Delete task 3"

### Technical Architecture
- **Backend**: FastAPI with PostgreSQL database
- **AI Integration**: Google Gemini API or Hugging Face Inference API with MCP tools
- **Frontend**: Next.js with React
- **Authentication**: JWT-based authentication
- **Data Storage**: SQLModel for ORM operations
- **MCP Server**: Dedicated server running on port 8001 for AI tool execution

## Requirements

- Node.js 18+
- Python 3.9+
- PostgreSQL database
- OpenAI API key

## Setup

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```
4. Configure environment variables (see `.env.example`) including:
   - OPENAI_API_KEY for AI integration
   - MCP_SERVER_PORT for the MCP server
5. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
6. Start the MCP server separately:
   ```bash
   cd backend
   python -m mcp_server.server
   ```
7. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Database models
│   │   ├── task.py          # Task model
│   │   ├── user.py          # User model
│   │   ├── conversation.py  # Conversation model for chatbot
│   │   ├── message.py       # Message model for chatbot
│   │   └── chat.py          # Chat models
│   ├── api/                 # API routes
│   │   └── chat.py          # Chat API endpoints
│   ├── services/            # Business logic
│   │   ├── task_service.py  # Task operations
│   │   ├── conversation_service.py  # Conversation operations
│   │   └── message_service.py       # Message operations
│   ├── tools/               # MCP tools for AI integration
│   │   ├── add_task.py      # Add task tool
│   │   ├── list_tasks.py    # List tasks tool
│   │   ├── complete_task.py # Complete task tool
│   │   ├── update_task.py   # Update task tool
│   │   ├── delete_task.py   # Delete task tool
│   │   └── validation.py    # Input validation
│   ├── agent/               # AI agent integration
│   │   └── chat_agent.py    # OpenAI agent implementation
│   ├── mcp_server/          # MCP protocol server
│   │   └── server.py        # MCP server implementation
│   ├── utils/               # Utility functions
│   └── middleware/          # Middleware components
├── frontend/                # Next.js frontend
│   ├── pages/               # Page components
│   ├── components/          # Reusable components
│   ├── lib/                 # Utilities and API clients
│   └── styles/              # Styling
└── README.md                # Project documentation
```