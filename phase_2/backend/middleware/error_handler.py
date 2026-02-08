"""
Global error handler middleware for the Todo Web Application.
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

try:
    from ..core.exceptions import TodoException
except ImportError:
    from core.exceptions import TodoException


# Set up logging
logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions.

    Args:
        request: The incoming request
        exc: The exception that occurred

    Returns:
        JSONResponse: A standardized error response
    """
    logger.error(f"Unhandled exception occurred: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handler for HTTP exceptions.

    Args:
        request: The incoming request
        exc: The HTTP exception that occurred

    Returns:
        JSONResponse: A standardized error response
    """
    logger.warning(f"HTTP exception {exc.status_code} occurred: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": f"HTTP_{exc.status_code}"
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler for request validation exceptions.

    Args:
        request: The incoming request
        exc: The validation exception that occurred

    Returns:
        JSONResponse: A standardized error response
    """
    logger.warning(f"Validation error occurred: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "error_code": "VALIDATION_ERROR"
        }
    )


async def todo_exception_handler(request: Request, exc: TodoException):
    """
    Handler for custom Todo application exceptions.

    Args:
        request: The incoming request
        exc: The custom Todo exception that occurred

    Returns:
        JSONResponse: A standardized error response
    """
    logger.info(f"Todo application error: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code
        }
    )