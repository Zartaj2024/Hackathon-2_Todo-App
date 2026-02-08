"""
FastAPI chat endpoints for the AI-Powered Chatbot feature.
Implements the chat endpoint as specified in the plan.md.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime

from chat_models.chat import ChatRequest, ChatResponse, ChatMessage
from models.user import User
from auth_enhanced import get_current_user, get_current_user_id
from chat_agent_pkg.chat_agent import chat_agent
from chat_services.conversation_service import conversation_service
from chat_services.message_service import message_service
from models.conversation import ConversationCreate
from models.message import MessageCreate


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/users", tags=["chat"])


@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    authenticated_user_id: str = Depends(get_current_user_id)
):
    """
    Main chat endpoint that integrates with Hugging Face Agent.
    Validates user authentication and routes to AI agent.

    Args:
        user_id: User ID from the path parameter
        chat_request: Chat request containing messages
        authenticated_user_id: Currently authenticated user ID (from JWT)

    Returns:
        ChatResponse: Response from the AI agent
    """
    logger.info(f"Received chat request for user {user_id}")

    # Verify user_id matches authenticated user
    if authenticated_user_id != user_id:
        logger.warning(f"Unauthorized access attempt for user {user_id}")
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Create conversation context
    conversation_context = {
        "user_id": user_id,
        "messages": [msg.model_dump() for msg in chat_request.messages]
    }

    # Add detailed error handling to identify the exact location of the error
    try:
        logger.debug(f"Processing conversation for user {user_id} with {len(chat_request.messages)} messages")
        
        # Debug logging
        messages_list = [msg.model_dump() for msg in chat_request.messages]
        logger.info(f"=== CHAT DEBUG === user_id: {user_id}")
        logger.info(f"=== CHAT DEBUG === messages_list type: {type(messages_list)}, length: {len(messages_list)}")
        logger.info(f"=== CHAT DEBUG === chat_agent instance: {chat_agent}")
        logger.info(f"=== CHAT DEBUG === About to call: chat_agent.process_conversation(user_id={user_id}, messages={messages_list})")

        # Process the conversation with the AI agent
        agent_response = await chat_agent.process_conversation(
            user_id, 
            messages_list
        )
        
        logger.info(f"=== CHAT DEBUG === Successfully received agent_response: {agent_response[:100] if agent_response else 'None'}")

        # Step 1: Create conversation in the database
        try:
            from database import Session, engine
            with Session(engine) as db_session:
                # Check if there's an existing active conversation or create a new one
                # For simplicity, we'll create a new one each time
                conversation_data = ConversationCreate(
                    user_id=user_id,
                    title=chat_request.messages[0].content[:50] if chat_request.messages else "Chat conversation"
                )
                conversation = conversation_service.create_conversation(db_session, conversation_data)
                logger.info(f"Conversation created successfully: {conversation.id}")
        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}", exc_info=True)
            raise

        # Step 2: Create and save messages - this is likely where the error occurs
        try:
            from database import Session, engine
            with Session(engine) as db_session:
                # Import Message model to create objects directly
                from models.message import Message

                # Save the user's messages directly without using MessageCreate to avoid inheritance issues
                for msg in chat_request.messages:
                    try:
                        # Create Message object and set fields individually to avoid field order issues
                        user_message = Message()
                        user_message.conversation_id = conversation.id
                        user_message.role = msg.role
                        user_message.content = msg.content
                        user_message.message_type = "text"  # Use string value instead of enum
                        user_message.metadata_json = None  # Set explicitly to avoid any defaults issues

                        db_session.add(user_message)
                        db_session.commit()
                        db_session.refresh(user_message)
                        logger.info(f"User message saved successfully")
                    except Exception as e:
                        logger.error(f"Error saving user message: {str(e)}", exc_info=True)
                        raise

                # Save the agent's response directly without using MessageCreate
                try:
                    agent_message = Message()
                    agent_message.conversation_id = conversation.id
                    agent_message.role = "assistant"
                    agent_message.content = agent_response
                    agent_message.message_type = "response"  # Use string value instead of enum
                    agent_message.metadata_json = None  # Set explicitly to avoid any defaults issues

                    db_session.add(agent_message)
                    db_session.commit()
                    db_session.refresh(agent_message)
                    logger.info(f"Agent message saved successfully")
                except Exception as e:
                    logger.error(f"Error saving agent message: {str(e)}", exc_info=True)
                    raise

        except Exception as e:
            logger.error(f"Error in message creation section: {str(e)}", exc_info=True)
            raise

        # Format the response
        response_messages = [
            ChatMessage(role="assistant", content=agent_response, timestamp=datetime.now())
        ]

        logger.info(f"Returning response for user {user_id}, conversation {conversation.id}")

        return ChatResponse(
            messages=response_messages,
            conversation_id=conversation.id
        )

    except Exception as e:
        logger.error(f"Detailed error in chat endpoint: {str(e)}", exc_info=True)
        # Provide more specific error details
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/{user_id}/chat/conversations")
async def get_user_conversations(
    user_id: str,
    authenticated_user_id: str = Depends(get_current_user_id)
):
    """
    Get all conversations for a user.

    Args:
        user_id: User ID from the path parameter
        authenticated_user_id: Currently authenticated user ID (from JWT)

    Returns:
        List of user's conversations
    """
    try:
        logger.info(f"Getting conversations for user {user_id}, authenticated as {authenticated_user_id}")

        # Verify user_id matches authenticated user
        if authenticated_user_id != user_id:
            logger.warning(f"Unauthorized access attempt for user {user_id}, authenticated as {authenticated_user_id}")
            raise HTTPException(status_code=403, detail="Unauthorized access")

        # Fetch conversations from the database
        try:
            from database import Session, engine
            with Session(engine) as db_session:
                conversations = conversation_service.get_user_conversations(db_session, user_id)
            logger.info(f"Successfully retrieved {len(conversations) if conversations else 0} conversations for user {user_id}")
            return conversations
        except Exception as db_error:
            logger.error(f"Database error retrieving conversations for user {user_id}: {str(db_error)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving conversations: {str(db_error)}"
            )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving conversations for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversations: {str(e)}"
        )


@router.get("/{user_id}/chat/conversation/{conversation_id}")
async def get_conversation(
    user_id: str,
    conversation_id: str,
    authenticated_user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific conversation with its messages.

    Args:
        user_id: User ID from the path parameter
        conversation_id: ID of the conversation to retrieve
        authenticated_user_id: Currently authenticated user ID (from JWT)

    Returns:
        Conversation with its messages
    """
    try:
        logger.info(f"Getting conversation {conversation_id} for user {user_id}, authenticated as {authenticated_user_id}")

        # Verify user_id matches authenticated user
        if authenticated_user_id != user_id:
            logger.warning(f"Unauthorized access attempt for user {user_id}, authenticated as {authenticated_user_id}")
            raise HTTPException(status_code=403, detail="Unauthorized access")

        # Fetch conversation and messages from the database
        try:
            from database import Session, engine
            with Session(engine) as db_session:
                # Get conversation
                conversation = conversation_service.get_conversation_by_id(
                    db_session,
                    conversation_id,
                    user_id
                )

                if not conversation:
                    logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
                    raise HTTPException(status_code=404, detail="Conversation not found")

                # Get messages for the conversation
                messages = message_service.get_messages_by_conversation(
                    db_session,
                    conversation_id,
                    user_id
                )

            logger.info(f"Successfully retrieved conversation {conversation_id} with {len(messages) if messages else 0} messages for user {user_id}")
            return {
                "conversation": conversation,
                "messages": messages
            }
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as db_error:
            logger.error(f"Database error retrieving conversation {conversation_id} for user {user_id}: {str(db_error)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving conversation: {str(db_error)}"
            )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving conversation {conversation_id} for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversation: {str(e)}"
        )


@router.get("/{user_id}/chat/token")
async def generate_chat_token(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a token for chat authentication if needed for frontend components.

    Args:
        user_id: User ID from the path parameter
        current_user: Currently authenticated user (from JWT)

    Returns:
        Token for chat authentication
    """
    try:
        logger.info(f"Generating chat token for user {user_id}, current user {current_user.id}")

        # Verify user_id matches authenticated user
        if current_user.id != user_id:
            logger.warning(f"Unauthorized token request for user {user_id}, current user {current_user.id}")
            raise HTTPException(status_code=403, detail="Unauthorized access")

        # In a real implementation, you would generate a temporary token
        # For now, we'll just return a success response
        logger.info(f"Successfully generated chat token response for user {user_id}")
        return {
            "success": True,
            "message": "Token generation endpoint - would return token in real implementation"
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating chat token for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating chat token: {str(e)}"
        )