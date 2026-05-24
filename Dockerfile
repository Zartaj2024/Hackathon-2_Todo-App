# Stage 1: Build Next.js frontend
FROM node:18-slim AS frontend-builder
WORKDIR /app
COPY phase_2/frontend/package*.json ./phase_2/frontend/
RUN cd phase_2/frontend && npm install
COPY phase_2/frontend ./phase_2/frontend
RUN cd phase_2/frontend && npm run build

# Stage 2: Python environment
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for running Next.js in production
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY phase_2/backend ./phase_2/backend
COPY phase_3/backend ./phase_3/backend
COPY phase_1/src ./phase_1/src

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/phase_2/frontend ./phase_2/frontend

# Copy start script
COPY start.sh .
RUN chmod +x start.sh

# Create data directory for SQLite
RUN mkdir -p /app/data && chmod 777 /app/data

# Environment variables
ENV PYTHONPATH="/app/phase_2/backend:/app/phase_3/backend"
ENV DATABASE_URL="sqlite:////app/data/todo_app.db"
ENV PORT=7860

# Expose the port Hugging Face expects
EXPOSE 7860

# Use start script
CMD ["./start.sh"]
