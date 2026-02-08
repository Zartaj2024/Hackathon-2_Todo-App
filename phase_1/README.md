# Multi-User Todo Web Application

A full-stack web application that allows multiple users to manage their personal tasks with secure authentication and proper task ownership enforcement.

## Features

- User registration and authentication with JWT tokens
- Create, read, update, and delete personal tasks
- Mark tasks as complete/incomplete
- Secure task ownership (users can only see and modify their own tasks)
- Responsive web interface

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI (Python) with SQLModel ORM
- **Database**: PostgreSQL
- **Authentication**: Better Auth with JWT tokens

## Requirements

- Node.js 18+
- Python 3.9+
- PostgreSQL database

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
4. Configure environment variables (see `.env.example`)
5. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
6. Start the frontend development server:
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
│   ├── api/                 # API routes
│   ├── services/            # Business logic
│   ├── utils/               # Utility functions
│   └── middleware/          # Middleware components
├── frontend/                # Next.js frontend
│   ├── pages/               # Page components
│   ├── components/          # Reusable components
│   ├── lib/                 # Utilities and API clients
│   └── styles/              # Styling
└── README.md                # Project documentation
```