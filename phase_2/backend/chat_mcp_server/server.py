"""
MCP Server for the AI-Powered Chatbot feature.
Implements the MCP protocol server to handle tool requests on port 8001.
"""

import asyncio
import json
from typing import Dict, Any, Callable
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from chat_tools import MCP_TOOLS

app = FastAPI(title="AI Chatbot MCP Tools Server", version="1.0.0")


class ToolRequest(BaseModel):
    """
    Request model for MCP tool calls.
    """
    tool_name: str
    user_id: str
    parameters: Dict[str, Any]


@app.post("/tools/{tool_name}")
async def handle_tool_call(tool_name: str, request: ToolRequest):
    """
    Handle MCP tool calls with user authentication and authorization.

    Args:
        tool_name: Name of the tool to execute
        request: Tool request containing user_id and parameters

    Returns:
        Tool execution result
    """
    # Verify that the tool exists
    if tool_name not in MCP_TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    # Get the tool handler
    tool_handler = MCP_TOOLS[tool_name]

    try:
        # Execute the tool with the provided parameters and user context
        result = await tool_handler(request.user_id, request.parameters)
        return result
    except Exception as e:
        # Return standardized error response as specified in error-strategy.md
        return {
            "success": False,
            "error": f"Tool execution failed: {str(e)}"
        }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for the MCP server.
    """
    return {"status": "healthy", "service": "mcp-tools-server"}


@app.get("/")
async def server_info():
    """
    Server information endpoint showing available tools.
    """
    available_tools = list(MCP_TOOLS.keys())
    return {
        "service": "AI Chatbot MCP Tools Server",
        "version": "1.0.0",
        "available_tools": available_tools
    }


def start_server(host: str = "0.0.0.0", port: int = 8001):
    """
    Start the MCP server on the specified host and port.

    Args:
        host: Host to bind the server to (default: 0.0.0.0)
        port: Port to run the server on (default: 8001 as specified in plan.md)
    """
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    # Run the server when executed directly
    start_server()