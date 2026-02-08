"""
Pydantic models for Natural Language Processing functionality in the Todo Web Application.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class NLPRequest(BaseModel):
    """
    Request model for natural language task creation.
    """
    text: str
    context: Optional[Dict[str, Any]] = None


class NLPResponse(BaseModel):
    """
    Response model for natural language processing results.
    """
    title: str
    description: str
    due_date: Optional[str] = None
    priority: str = "medium"
    tags: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    parsed_entities: Optional[Dict[str, Any]] = None


class PrioritySuggestionRequest(BaseModel):
    """
    Request model for priority suggestion.
    """
    title: str
    description: Optional[str] = ""
    due_date: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class PrioritySuggestionResponse(BaseModel):
    """
    Response model for priority suggestions.
    """
    priority: str
    confidence: float
    score: float
    factors: Dict[str, float]
    reasoning: str