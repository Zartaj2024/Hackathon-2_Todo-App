"""
OpenAI Agent SDK integration for the AI-Powered Chatbot feature.
Implements the agent with system instructions and tool binding.
"""

import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from pydantic import BaseModel

from chat_tools import MCP_TOOLS


class ChatMessage(BaseModel):
    """
    Model for chat messages in the conversation.
    """
    role: str  # "user" or "assistant"
    content: str


class AgentConfig:
    """
    Configuration for the OpenAI agent.
    """
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"  # Using a modern, capable model
        self.temperature = 0.3  # Lower temperature for more consistent responses
        self.max_tokens = 1000  # Reasonable limit for task management responses


class ChatAgent:
    """
    OpenAI Agent for handling task management conversations.
    """

    def __init__(self):
        self.config = AgentConfig()
        self.tools = self._prepare_tools()

    def _prepare_tools(self) -> List[Dict[str, Any]]:
        """
        Prepare tool definitions for the OpenAI agent based on MCP tools.

        Returns:
            List of tool definitions compatible with OpenAI function calling
        """
        # Define the tools that match the MCP tools
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the task to be created",
                                "minLength": 1,
                                "maxLength": 255
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of the task (optional)",
                                "maxLength": 1000
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Priority level of the task (optional, defaults to medium)",
                                "default": "medium"
                            },
                            "due_date": {
                                "type": "string",
                                "format": "date",
                                "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                                "description": "Due date in YYYY-MM-DD format (optional)"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["all", "completed", "pending"],
                                "description": "Filter tasks by completion status (optional, defaults to all)",
                                "default": "all"
                            },
                            "limit": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 100,
                                "description": "Maximum number of tasks to return (optional, defaults to 10)",
                                "default": 10
                            },
                            "offset": {
                                "type": "integer",
                                "minimum": 0,
                                "description": "Number of tasks to skip (for pagination, optional)",
                                "default": 0
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a specific task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "ID of the task to mark as completed"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task with new information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "minLength": 1,
                                "maxLength": 255,
                                "description": "New title for the task (optional)"
                            },
                            "description": {
                                "type": "string",
                                "maxLength": 1000,
                                "description": "New description for the task (optional)"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New priority level (optional)"
                            },
                            "due_date": {
                                "type": "string",
                                "format": "date",
                                "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                                "description": "New due date in YYYY-MM-DD format (optional)"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Whether the task is completed (optional)"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task from the user's task list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

        return openai_tools

    def _get_system_prompt(self) -> str:
        """
        Get the system prompt with instructions for task management.

        Returns:
            System prompt string
        """
        return """
        You are an AI assistant specialized in helping users manage their tasks.
        Your purpose is to interpret natural language requests and perform appropriate task management operations.

        Guidelines:
        1. Always interpret user requests in the context of task management
        2. Use the appropriate tool for each request:
           - Use add_task for adding new tasks
           - Use list_tasks for showing user's tasks
           - Use complete_task for marking tasks as done
           - Use update_task for modifying existing tasks
           - Use delete_task for removing tasks
        3. If a user wants to see their tasks, use list_tasks
        4. If a user mentions a task number, always use that number in your tool calls
        5. Be helpful and provide clear responses
        6. If you're unsure about something, ask for clarification

        Remember to respect user privacy and only operate on their own tasks.
        """

    async def process_conversation(self, user_id: str, messages: List[Dict[str, str]]) -> str:
        """
        Process a conversation with the OpenAI agent.

        Args:
            user_id: ID of the authenticated user
            messages: List of messages in the conversation

        Returns:
            Agent's response to the conversation
        """
        # Prepare the messages for the API call
        prepared_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages
        ]

        # Add the system message at the beginning
        prepared_messages.insert(0, {
            "role": "system",
            "content": self._get_system_prompt()
        })

        try:
            # Make the API call with the tools
            response = self.config.client.chat.completions.create(
                model=self.config.model,
                messages=prepared_messages,
                tools=self.tools,
                tool_choice="auto",
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Process tool calls
                final_response = await self._process_tool_calls(user_id, tool_calls)
                return final_response
            else:
                # Return the assistant's message if no tools were called
                return response_message.content or "I'm here to help you manage your tasks. How can I assist you today?"

        except Exception as e:
            # Handle errors gracefully and return a helpful message
            return f"I'm currently experiencing technical difficulties. Please try again in a moment. Error: {str(e)}"

    async def _process_tool_calls(self, user_id: str, tool_calls) -> str:
        """
        Process the tool calls made by the agent.

        Args:
            user_id: ID of the authenticated user
            tool_calls: Tool calls made by the agent

        Returns:
            Formatted response based on tool call results
        """
        # This is a simplified implementation - in a real system, you would need to
        # actually execute the tools and return the results to the agent for follow-up
        results = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # In a real implementation, you would call the actual tool function
            # For now, we'll simulate the response
            if function_name in MCP_TOOLS:
                # Execute the tool with user context
                try:
                    result = await MCP_TOOLS[function_name](user_id, function_args)
                    results.append(f"{function_name}: {result}")
                except Exception as e:
                    results.append(f"Error calling {function_name}: {str(e)}")
            else:
                results.append(f"Unknown tool: {function_name}")

        # Combine results into a response
        if results:
            return " ".join(results)
        else:
            return "I processed your request but didn't make any changes to your tasks."


# Global instance of the agent
chat_agent = ChatAgent()