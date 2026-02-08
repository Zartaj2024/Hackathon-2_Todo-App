"""
FastAPI application entry point for the Todo Web Application.
"""

from fastapi import FastAPI, Depends, HTTPException, status
import logging
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime
import logging

from config import settings
from database import create_db_and_tables
from api.routers import auth, tasks
from chat_api import chat
from api.nlp_tasks import router as nlp_tasks_router  # Import the new NLP tasks router

# Import error handlers
from middleware.error_handler import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    todo_exception_handler
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to initialize the database tables on startup.
    """
    logger = logging.getLogger(__name__)
    logger.info("Application starting up...")
    try:
        print("Creating database tables...")
        logger.info("Creating database tables...")
        create_db_and_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}", exc_info=True)
        print(f"Error creating database tables: {e}")
        raise
    yield
    logger.info("Application shutting down...")
    print("Shutting down...")


# Create the FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="A multi-user todo web application with authentication and task management",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Todo App Support",
        "url": "http://todo-app.local/support",
        "email": "support@todoapp.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add rate limit exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    # Additional security headers
    allow_origin_regex=None,
    expose_headers=["Access-Control-Allow-Origin"]
)


# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks")
# The chat router has prefix /users, so with API_V1_STR it becomes /api/v1/users/{user_id}/chat
app.include_router(chat.router, prefix=settings.API_V1_STR)
# Include the new NLP tasks router - add to tasks endpoints
app.include_router(nlp_tasks_router, prefix=f"{settings.API_V1_STR}/tasks")


# Register exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Import and add custom exception handler
from core.exceptions import TodoException
app.add_exception_handler(TodoException, todo_exception_handler)


@app.get("/")
async def root():
    """
    Root endpoint for the API.

    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Welcome to the Todo Web Application API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the application is running.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "todo-web-application-api",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint to verify the application is ready to serve traffic.

    Returns:
        dict: Readiness status information
    """
    # Add any additional readiness checks here (e.g., database connectivity)
    return {
        "status": "ready",
        "service": "todo-web-application-api",
        "timestamp": datetime.utcnow().isoformat()
    }


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)