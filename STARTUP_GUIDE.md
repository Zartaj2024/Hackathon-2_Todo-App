# Startup Guide for Todo App

Follow these 3 steps to start the full application with backend API, Next.js frontend, and CLI.

## Step 1: Start the Backend API Server

Open a terminal/command prompt and run:

```bash
cd phase_2/backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

This starts the FastAPI backend server on `http://localhost:8000`.
Keep this terminal running - the backend must stay active.

## Step 2: Start the Next.js Frontend

Open a **second** terminal/command prompt and run:

```bash
cd phase_2/frontend
npm install
npm run dev
```

This starts the Next.js frontend on `http://localhost:3000`.
The frontend will connect to the backend API automatically.

## Step 3: Use the CLI Application

Open a **third** terminal/command prompt and run:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/phase_1
cd phase_1/src
python main.py
```

This starts the CLI application that also connects to the same backend API.

## Access the Applications

- **Backend API**: `http://localhost:8000` (with API documentation at `/docs`)
- **Web Frontend**: `http://localhost:3000`
- **CLI Application**: Terminal interface in the third terminal

All three interfaces share the same backend database and user accounts.