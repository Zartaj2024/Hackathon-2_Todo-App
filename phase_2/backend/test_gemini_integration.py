"""
Test script to verify Gemini API integration with the chat agent.
"""

import asyncio
import os
from chat_agent_pkg.chat_agent import ChatAgent


async def test_gemini_integration():
    """
    Test the Gemini API integration by simulating a conversation.
    """
    print("Testing Gemini API integration...")
    
    # Create an instance of the chat agent
    agent = ChatAgent()
    
    print(f"AI Provider configured: {agent.config.ai_provider}")
    print(f"Model name: {agent.config.model_name}")
    
    if agent.config.ai_provider == "gemini":
        print("Gemini API key presence:", bool(agent.config.api_key))
    else:
        print("Using fallback provider")
    
    # Simulate a conversation
    user_id = "test_user_123"
    messages = [
        {"role": "user", "content": "Hello, I'd like to add a task to buy groceries."}
    ]
    
    try:
        response = await agent.process_conversation(user_id, messages)
        print(f"Agent response: {response}")
        print("Gemini integration test: PASSED")
        return True
    except Exception as e:
        print(f"Gemini integration test: FAILED - Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Set the AI provider to Gemini for testing
    os.environ["AI_PROVIDER"] = "gemini"
    
    # Note: This test will only work if you have a valid GEMINI_API_KEY in your environment
    # For a real test, you would need to set the environment variable:
    # os.environ["GEMINI_API_KEY"] = "your_actual_api_key_here"
    
    success = asyncio.run(test_gemini_integration())
    
    if success:
        print("\nIntegration test completed successfully!")
    else:
        print("\nIntegration test failed. Please check your configuration.")