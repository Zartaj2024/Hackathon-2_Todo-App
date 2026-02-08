"""
Startup script for the Todo Web Application backend.
This script handles application initialization and startup procedures.
"""

import uvicorn
import asyncio
from .main import app
from .config import settings


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    Run the FastAPI server with the specified configuration.

    Args:
        host: Host address to bind the server to
        port: Port number to listen on
        reload: Whether to enable auto-reload during development
    """
    print(f"Starting Todo Web Application server on {host}:{port}")
    print(f"Environment: {'development' if reload else 'production'}")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=["."] if reload else None,
        log_level="info"
    )


def main():
    """
    Main entry point for the application.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Todo Web Application Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host address (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port number (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload (development)')

    args = parser.parse_args()

    run_server(host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()