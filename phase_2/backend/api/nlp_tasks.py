"""
Natural Language Processing API endpoints for task creation and prioritization.
Implements the NLP and AI prioritization features as specified in the todo app requirements.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Generator
from contextlib import contextmanager

from models.task import TaskCreate, TaskRead
from models.user import User
from models.nlp_models import NLPRequest as NLPRequestModel, PrioritySuggestionRequest, PrioritySuggestionResponse
from auth_enhanced import get_current_user, get_current_user_id
from services.task_service import create_task
from database import Session, engine

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["nlp-tasks"])

@router.post("/nlp")
async def create_task_from_natural_language(
    nlp_request: NLPRequestModel,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Create a task from natural language input with AI-powered prioritization.

    Args:
        nlp_request: Request containing natural language text and optional context
        current_user_id: ID of the authenticated user (from JWT)

    Returns:
        TaskRead: Created task with AI-suggested priority
    """
    try:
        logger.info(f"Processing NLP task creation request for user {current_user_id}")

        # Extract natural language text from request
        natural_language_text = nlp_request.text
        if not natural_language_text:
            raise HTTPException(
                status_code=400,
                detail="Missing 'text' in request body"
            )

        # Parse the natural language to extract task components
        from nlp_processor import parse_task_from_natural_language
        parsed_result = parse_task_from_natural_language(natural_language_text)

        # Use AI to suggest priority based on task details
        from priority_engine import suggest_smart_priority
        priority_suggestion = suggest_smart_priority(
            title=parsed_result.get('title', ''),
            description=parsed_result.get('description', ''),
            due_date=parsed_result.get('due_date'),
            user_context={"user_id": current_user_id}
        )

        # Create the task with AI-suggested priority
        task_create_data = TaskCreate(
            title=parsed_result.get('title', '')[:255],  # Ensure title is within length limits
            description=parsed_result.get('description', ''),
            completed=False,
            user_id=current_user_id,
            priority=priority_suggestion.get('priority', 'medium'),  # Use AI-suggested priority
            due_date=parsed_result.get('due_date')
        )

        # Create the task in the database
        from database import Session, engine
        from sqlmodel import Session as SQLModelSession

        with SQLModelSession(engine) as db_session:
            created_task = create_task(db_session, task_create_data)
            db_session.commit()
            db_session.refresh(created_task)

        # Add priority information to the response
        response_data = TaskRead.model_validate(created_task)

        logger.info(f"Task created successfully from NLP: {created_task.id}")
        return response_data

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error creating task from NLP: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing natural language task: {str(e)}"
        )


@router.post("/prioritize")
async def get_priority_suggestion(
    task_data: PrioritySuggestionRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get AI-powered priority suggestion for a task based on its details.

    Args:
        task_data: Dictionary containing task details (title, description, due_date)
        current_user_id: ID of the authenticated user (from JWT)

    Returns:
        Dict: Priority suggestion with confidence and reasoning
    """
    try:
        logger.info(f"Getting priority suggestion for user {current_user_id}")

        title = task_data.title
        description = task_data.description
        due_date = task_data.due_date

        if not title:
            raise HTTPException(
                status_code=400,
                detail="Missing 'title' in request body"
            )

        # Get priority suggestion from AI
        from priority_engine import suggest_smart_priority
        priority_suggestion = suggest_smart_priority(
            title=title,
            description=description,
            due_date=due_date,
            user_context={"user_id": current_user_id}
        )

        logger.info(f"Priority suggestion generated: {priority_suggestion['priority']} with confidence {priority_suggestion['confidence']}")
        return priority_suggestion

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error generating priority suggestion: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating priority suggestion: {str(e)}"
        )


@router.post("/nlp/batch")
async def create_multiple_tasks_from_natural_language(
    batch_request: Dict[str, Any],
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Create multiple tasks from a natural language input that describes several tasks.

    Args:
        batch_request: Dictionary containing natural language text for multiple tasks
        current_user_id: ID of the authenticated user (from JWT)

    Returns:
        List[TaskRead]: List of created tasks with AI-suggested priorities
    """
    try:
        logger.info(f"Processing batch NLP task creation for user {current_user_id}")

        natural_language_text = batch_request.get("text", "")
        if not natural_language_text:
            raise HTTPException(
                status_code=400,
                detail="Missing 'text' in request body"
            )

        # For now, we'll just create a single task from the text
        # In a more advanced implementation, we would parse multiple tasks from the text
        from nlp_processor import parse_task_from_natural_language
        parsed_result = parse_task_from_natural_language(natural_language_text)

        # Use AI to suggest priority
        from priority_engine import suggest_smart_priority
        priority_suggestion = suggest_smart_priority(
            title=parsed_result.get('title', ''),
            description=parsed_result.get('description', ''),
            due_date=parsed_result.get('due_date'),
            user_context={"user_id": current_user_id}
        )

        # Create the task
        task_create_data = TaskCreate(
            title=parsed_result.get('title', '')[:255],  # Ensure title is within length limits
            description=parsed_result.get('description', ''),
            completed=False,
            user_id=current_user_id,
            priority=priority_suggestion.get('priority', 'medium'),
            due_date=parsed_result.get('due_date')
        )

        # Create the task in the database
        from database import Session, engine
        from sqlmodel import Session as SQLModelSession

        with SQLModelSession(engine) as db_session:
            created_task = create_task(db_session, task_create_data)
            db_session.commit()
            db_session.refresh(created_task)

        # Add priority information to the response
        response_data = TaskRead.model_validate(created_task)

        logger.info(f"Batch task created successfully: {created_task.id}")
        return [response_data]

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error creating batch tasks from NLP: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing natural language tasks: {str(e)}"
        )