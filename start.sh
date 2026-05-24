#!/bin/bash

# Start the Backend
echo "Starting Backend..."
export PYTHONPATH=$PYTHONPATH:/app/phase_2/backend:/app/phase_3/backend
export DATABASE_URL=sqlite:////app/data/todo_app.db
mkdir -p /app/data

# Initialize DB if needed
python3 -m phase_2.backend.init_db

python3 -m uvicorn phase_2.backend.main:app --host 0.0.0.0 --port 8000 &

# Start the MCP Server
echo "Starting MCP Server..."
python3 -m phase_3.backend.chat_mcp_server.server --host 0.0.0.0 --port 8001 &

# Start the Frontend
echo "Starting Frontend..."
cd /app/phase_2/frontend
# Run next start on 7860 as expected by Hugging Face
npm run start -- --port 7860 &

# Wait for any process to exit
wait -n

# Exit with status of the process that crashed
exit $?
