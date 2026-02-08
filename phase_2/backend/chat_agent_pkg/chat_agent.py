"""
Google Gemini API integration for the AI-Powered Chatbot feature.
Implements the agent with system instructions and tool binding.
Supports both Gemini and Hugging Face as AI providers.
"""

import os
import json
import requests
from typing import List, Dict, Any
from pydantic import BaseModel
import asyncio

from chat_tools import MCP_TOOLS
import google.generativeai as genai
from config import settings


class ChatMessage(BaseModel):
    """
    Model for chat messages in the conversation.
    """
    role: str  # "user" or "assistant"
    content: str


class AgentConfig:
    """
    Configuration for the AI agent supporting both Gemini and Hugging Face.
    """
    def __init__(self):
        self.ai_provider = settings.AI_PROVIDER.lower()
        
        if self.ai_provider == "gemini":
            self.model_name = settings.GEMINI_MODEL_NAME
            self.api_key = settings.GEMINI_API_KEY
            self.temperature = 0.7
            self.max_tokens = 2048  # Gemini supports larger response sizes
        else:  # Default to Hugging Face
            self.model_name = settings.HF_MODEL_NAME
            self.api_key = settings.HF_API_KEY
            self.temperature = 0.7
            self.max_tokens = 1000
            # Use environment variable for endpoint to match huggingface_hub library behavior
            hf_endpoint = os.getenv("HF_INFERENCE_ENDPOINT", "https://router.huggingface.co")
            self.hf_api_url = f"{hf_endpoint}/models/{self.model_name}"  # Hugging Face API URL


class ChatAgent:
    """
    AI Agent for handling task management conversations.
    Supports both Google Gemini and Hugging Face as providers.
    """

    def __init__(self):
        self.config = AgentConfig()
        
        if self.config.ai_provider == "gemini":
            # Initialize Gemini client
            genai.configure(api_key=self.config.api_key)
            self.gemini_client = genai.GenerativeModel(self.config.model_name)
        else:
            # For Hugging Face, we'll define a simpler approach since HF doesn't have the same tool calling mechanism as OpenAI
            pass

    def _prepare_tools(self) -> List[Dict[str, Any]]:
        """
        Prepare tool definitions for the Hugging Face agent based on MCP tools.
        This is kept for compatibility with the existing system but won't be used directly with HF.
        """
        # Define the tools that match the MCP tools for reference
        hf_tools = [
            {
                "name": "add_task",
                "description": "Add a new task for the user",
                "parameters": {
                    "title": {"type": "string", "required": True},
                    "description": {"type": "string", "required": False},
                    "priority": {"type": "string", "required": False},
                    "due_date": {"type": "string", "required": False}
                }
            },
            {
                "name": "list_tasks",
                "description": "List all tasks for the user",
                "parameters": {
                    "status": {"type": "string", "required": False},
                    "limit": {"type": "integer", "required": False},
                    "offset": {"type": "integer", "required": False}
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a specific task as completed",
                "parameters": {
                    "task_id": {"type": "integer", "required": True}
                }
            },
            {
                "name": "update_task",
                "description": "Update an existing task with new information",
                "parameters": {
                    "task_id": {"type": "integer", "required": True},
                    "title": {"type": "string", "required": False},
                    "description": {"type": "string", "required": False},
                    "priority": {"type": "string", "required": False},
                    "due_date": {"type": "string", "required": False},
                    "completed": {"type": "boolean", "required": False}
                }
            },
            {
                "name": "delete_task",
                "description": "Remove a task from the user's task list",
                "parameters": {
                    "task_id": {"type": "integer", "required": True}
                }
            }
        ]

        return hf_tools

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
        5. Be helpful and provide clear, concise responses
        6. If you're unsure about something, ask for clarification

        Remember to respect user privacy and only operate on their own tasks.
        """

    async def process_conversation(self, user_id: str, messages: List[Dict[str, str]]) -> str:
        """
        Process a conversation with the AI agent (either Gemini or Hugging Face).

        Args:
            user_id: ID of the authenticated user
            messages: List of messages in the conversation

        Returns:
            Agent's response to the conversation
        """
        if self.config.ai_provider == "gemini":
            return await self._process_with_gemini(user_id, messages)
        else:
            return await self._process_with_huggingface(user_id, messages)

    async def _process_with_gemini(self, user_id: str, messages: List[Dict[str, str]]) -> str:
        """
        Process a conversation with the Google Gemini agent.

        Args:
            user_id: ID of the authenticated user
            messages: List of messages in the conversation

        Returns:
            Agent's response to the conversation
        """
        try:
            # Prepare the prompt with system instructions and conversation history
            system_prompt = self._get_system_prompt()

            # Convert messages to Gemini format
            gemini_history = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"  # Gemini uses 'model' for assistant
                gemini_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

            # Create a chat session with the system instructions
            chat_session = self.gemini_client.start_chat(history=gemini_history)

            # Send a blank message to get the model's initial response based on history
            # Actually, we should send a new user message, so let's get the last user message
            last_user_message = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    last_user_message = msg["content"]
                    break

            if not last_user_message:
                last_user_message = "Hello"

            # Generate content based on the conversation history
            response = await self.gemini_client.generate_content_async(
                last_user_message,
                generation_config={
                    "temperature": self.config.temperature,
                    "max_output_tokens": self.config.max_tokens,
                }
            )

            if response and response.text:
                # Check if the generated text contains any tool-like commands
                # This is a simplified approach to detect if the model suggests using a tool
                tool_response = await self._detect_and_execute_tools(user_id, response.text)
                if tool_response:
                    return tool_response

                return response.text
            else:
                return "I'm here to help you manage your tasks. How can I assist you today?"

        except Exception as e:
            # Handle errors gracefully and return a helpful message
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            return f"I'm currently experiencing technical difficulties. Please try again in a moment. Error: {str(e)}"

    async def _process_with_huggingface(self, user_id: str, messages: List[Dict[str, str]]) -> str:
        """
        Process a conversation with the Hugging Face agent.

        Args:
            user_id: ID of the authenticated user
            messages: List of messages in the conversation

        Returns:
            Agent's response to the conversation
        """
        try:
            # Prepare the prompt with system instructions and conversation history
            system_prompt = self._get_system_prompt()

            # Format the conversation for Hugging Face
            # Combine system prompt with conversation history
            full_prompt = f"{system_prompt}\n\n"

            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                full_prompt += f"{role.capitalize()}: {content}\n"

            full_prompt += "Assistant:"

            # Prepare the payload for Hugging Face API
            # Different models may require different parameter formats
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": self.config.max_tokens,
                    "temperature": self.config.temperature,
                    "return_full_text": False,  # Only return the generated text
                    "truncation": True  # Truncate input if too long for the model
                }
            }

            # Prepare headers with API key for Hugging Face
            headers = {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            }

            # Make the API call to Hugging Face
            response = requests.post(
                self.config.hf_api_url,
                headers=headers,
                json=payload,
                timeout=30  # Add timeout for the request
            )

            if response.status_code == 200:
                result = response.json()

                # Extract the generated text from the response
                if isinstance(result, list) and len(result) > 0:
                    response_text = result[0].get("generated_text", "")
                else:
                    response_text = str(result) if result else ""

                if response_text:
                    # Check if the generated text contains any tool-like commands
                    # This is a simplified approach to detect if the model suggests using a tool
                    tool_response = await self._detect_and_execute_tools(user_id, response_text)
                    if tool_response:
                        return tool_response

                    return response_text
                else:
                    return "I'm here to help you manage your tasks. How can I assist you today?"
            elif response.status_code == 503:
                # Handle model loading case - Hugging Face returns 503 when model is loading
                return "The AI model is currently loading. Please try again in a moment."
            else:
                # Handle error response from Hugging Face API
                error_detail = response.text if response.text else f"HTTP {response.status_code}"
                # Log the specific error for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Hugging Face API error - Status: {response.status_code}, Detail: {error_detail}")
                logger.error(f"Hugging Face API error - URL: {self.config.hf_api_url}")
                logger.error(f"Hugging Face API error - Model: {self.config.model_name}")
                logger.error(f"Hugging Face API error - API Key present: {bool(self.config.api_key)}")

                # Check if it's a 404 error specifically for model not found
                if response.status_code == 404:
                    # Provide a fallback response instead of just an error
                    fallback_response = "I'm currently experiencing technical difficulties. The AI model is temporarily unavailable. Could you please try rephrasing your request or try again later?"
                    logger.warning(f"Model {self.config.model_name} not available, returning fallback response")
                    return fallback_response
                elif response.status_code == 429:
                    # Handle rate limiting
                    return "I'm currently experiencing high demand. Please wait a moment and try again."
                else:
                    return f"I'm currently experiencing technical difficulties. Please try again in a moment. Error: {error_detail}"

        except Exception as e:
            # Handle errors gracefully and return a helpful message
            return f"I'm currently experiencing technical difficulties. Please try again in a moment. Error: {str(e)}"

    async def _detect_and_execute_tools(self, user_id: str, generated_text: str) -> str:
        """
        Detect if the generated text contains tool commands and execute them.
        This is a simplified approach to mimic OpenAI's function calling with Hugging Face models.
        
        Args:
            user_id: ID of the authenticated user
            generated_text: Text generated by the Hugging Face model
            
        Returns:
            Formatted response based on tool execution or None if no tools were detected
        """
        # This is a simplified implementation that looks for patterns in the generated text
        # that might indicate tool usage. In a real implementation, you might use a more
        # sophisticated approach to parse the model's output for tool calls.
        
        # Look for patterns that suggest tool usage
        import re
        
        # Pattern to detect if the model suggests adding a task
        add_task_pattern = r'add_task\(["\']([^"\']+?)["\'](?:,\s*["\']([^"\']*?)["\'])?'
        list_tasks_pattern = r'list_tasks\(\)'
        complete_task_pattern = r'complete_task\((\d+)\)'
        update_task_pattern = r'update_task\((\d+)(?:,\s*["\']([^"\']*?)["\'])?'
        delete_task_pattern = r'delete_task\((\d+)\)'
        
        results = []
        
        # Check for add_task
        add_matches = re.findall(add_task_pattern, generated_text)
        for match in add_matches:
            title = match[0]
            description = match[1] if len(match) > 1 and match[1] else None
            
            try:
                # Prepare arguments for the tool
                args = {"title": title}
                if description:
                    args["description"] = description
                
                result = await MCP_TOOLS["add_task"](user_id, args)
                results.append(f"Added task: {result}")
            except Exception as e:
                results.append(f"Error adding task: {str(e)}")
        
        # Check for list_tasks
        if re.search(list_tasks_pattern, generated_text):
            try:
                result = await MCP_TOOLS["list_tasks"](user_id, {})
                results.append(f"Tasks: {result}")
            except Exception as e:
                results.append(f"Error listing tasks: {str(e)}")
        
        # Check for complete_task
        complete_matches = re.findall(complete_task_pattern, generated_text)
        for task_id in complete_matches:
            try:
                args = {"task_id": int(task_id)}
                result = await MCP_TOOLS["complete_task"](user_id, args)
                results.append(f"Completed task: {result}")
            except Exception as e:
                results.append(f"Error completing task: {str(e)}")
        
        # Check for delete_task
        delete_matches = re.findall(delete_task_pattern, generated_text)
        for task_id in delete_matches:
            try:
                args = {"task_id": int(task_id)}
                result = await MCP_TOOLS["delete_task"](user_id, args)
                results.append(f"Deleted task: {result}")
            except Exception as e:
                results.append(f"Error deleting task: {str(e)}")
        
        # Check for update_task
        update_matches = re.findall(update_task_pattern, generated_text)
        for match in update_matches:
            task_id = match[0]
            try:
                args = {"task_id": int(task_id)}
                if len(match) > 1 and match[1]:
                    args["title"] = match[1]
                
                result = await MCP_TOOLS["update_task"](user_id, args)
                results.append(f"Updated task: {result}")
            except Exception as e:
                results.append(f"Error updating task: {str(e)}")
        
        # Combine results into a response
        if results:
            return " ".join(results)
        else:
            return None  # No tools were detected in the generated text

    async def _process_tool_calls(self, user_id: str, tool_calls) -> str:
        """
        Process the tool calls made by the agent.
        This method is maintained for compatibility but won't be used with Hugging Face models.

        Args:
            user_id: ID of the authenticated user
            tool_calls: Tool calls made by the agent

        Returns:
            Formatted response based on tool call results
        """
        # This method is maintained for compatibility but Hugging Face models don't support
        # function calling in the same way as OpenAI, so this is a fallback implementation
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