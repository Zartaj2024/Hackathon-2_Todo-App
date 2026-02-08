# Startup Guide for Todo App

Follow these 3 steps to start the full application with backend API, Next.js frontend, and CLI.

## Step 1: Start the Backend API Server

Open a terminal/command prompt and run:

```bash
cd D:\zartaj\Todo_App\phase_2
python -m uvicorn backend.main:app --reload --port 8000
```

This starts the FastAPI backend server on `http://localhost:8000`.
Keep this terminal running - the backend must stay active.

## Step 2: Start the Next.js Frontend

Open a **second** terminal/command prompt and run:

```bash
cd D:\zartaj\Todo_App\todo_website
npm install
npm run dev
```

This starts the Next.js frontend on `http://localhost:3000`.
The frontend will connect to the backend API automatically.

## Step 3: Use the CLI Application

Open a **third** terminal/command prompt and run:

```bash
cd D:\zartaj\Todo_App\phase_1\src
python main.py
```

This starts the CLI application that also connects to the same backend API.

## Access the Applications

- **Backend API**: `http://localhost:8000` (with API documentation at `/docs`)
- **Web Frontend**: `http://localhost:3000`
- **CLI Application**: Terminal interface in the third terminal

All three interfaces share the same backend database and user accounts.