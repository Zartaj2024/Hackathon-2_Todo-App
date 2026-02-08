"""
AI Priority Engine for task prioritization in the Todo Web Application.
Uses ML models and rule-based systems to suggest task priorities based on various factors.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from enum import Enum

logger = logging.getLogger(__name__)

class PriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class PriorityEngine:
    """
    AI-powered priority engine that analyzes task details and user context to suggest priorities.
    """

    def __init__(self):
        # Define priority factors and their weights
        self.priority_factors = {
            'deadline_proximity': 0.35,  # Higher weight for urgent deadlines
            'keyword_importance': 0.30,  # Important keywords
            'task_duration': 0.10,      # Shorter tasks might be prioritized
            'user_history': 0.15,       # Based on user's past behavior
            'recurrence_pattern': 0.10  # Recurring tasks may have different priority
        }

    def calculate_priority(self, task_details: Dict, user_context: Dict = None) -> Dict[str, any]:
        """
        Calculate priority for a task based on various factors.

        Args:
            task_details: Dictionary containing task information
            user_context: Optional user context data

        Returns:
            Dict containing priority level, confidence score, and reasoning
        """
        try:
            logger.info(f"Calculating priority for task: {task_details.get('title', 'Unknown')}")

            # Initialize scores
            scores = {
                'deadline_proximity': 0.0,
                'keyword_importance': 0.0,
                'task_duration': 0.0,
                'user_history': 0.0,
                'recurrence_pattern': 0.0
            }

            # Calculate each factor score
            scores['deadline_proximity'] = self._calculate_deadline_proximity_score(task_details)
            scores['keyword_importance'] = self._calculate_keyword_importance_score(task_details)
            scores['task_duration'] = self._calculate_task_duration_score(task_details)

            if user_context:
                scores['user_history'] = self._calculate_user_history_score(task_details, user_context)
                scores['recurrence_pattern'] = self._calculate_recurrence_score(task_details, user_context)

            # Define the actual weights for each factor
            deadline_weight = 0.35
            keyword_weight = 0.30
            duration_weight = 0.10
            history_weight = 0.15
            recurrence_weight = 0.10

            # Calculate weighted average using the defined weights
            total_score = (
                scores['deadline_proximity'] * deadline_weight +
                scores['keyword_importance'] * keyword_weight +
                scores['task_duration'] * duration_weight +
                scores['user_history'] * history_weight +
                scores['recurrence_pattern'] * recurrence_weight
            )

            # Determine priority level
            if total_score >= 0.7:
                priority_level = PriorityLevel.HIGH
            elif total_score >= 0.4:
                priority_level = PriorityLevel.MEDIUM
            else:
                priority_level = PriorityLevel.LOW

            # Calculate confidence score
            confidence = min(total_score * 1.2, 1.0)  # Cap at 1.0

            # Generate reasoning
            reasoning = self._generate_reasoning(scores, task_details)

            result = {
                'priority': priority_level.value,
                'confidence': confidence,
                'score': total_score,
                'factors': scores,
                'reasoning': reasoning
            }

            logger.info(f"Priority calculated: {result}")
            return result

        except Exception as e:
            logger.error(f"Error calculating priority: {str(e)}", exc_info=True)
            # Return default values in case of error
            return {
                'priority': 'medium',
                'confidence': 0.5,
                'score': 0.5,
                'factors': {},
                'reasoning': 'Default priority assigned due to processing error'
            }

    def _calculate_deadline_proximity_score(self, task_details: Dict) -> float:
        """Calculate priority score based on deadline proximity."""
        due_date_str = task_details.get('due_date')
        if not due_date_str:
            return 0.3  # Default medium priority if no deadline

        try:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            time_diff = due_date - datetime.now()

            # If due today or in the past, high priority
            if time_diff.days <= 0:
                return 0.9

            # If due within 2 days, high-medium priority
            if time_diff.days <= 2:
                return 0.7

            # If due within a week, medium priority
            if time_diff.days <= 7:
                return 0.5

            # If due later, lower priority
            return 0.2

        except Exception as e:
            logger.warning(f"Error parsing due date {due_date_str}: {str(e)}")
            return 0.3  # Default medium priority

    def _calculate_keyword_importance_score(self, task_details: Dict) -> float:
        """Calculate priority score based on important keywords."""
        title = task_details.get('title', '')
        description = task_details.get('description', '')
        text = (title + ' ' + description).lower()

        # High importance keywords
        high_imp_words = [
            'urgent', 'asap', 'immediately', 'important', 'critical', 'priority',
            'deadline', 'emergency', 'crucial', 'essential', 'vital', 'pressing',
            'time-sensitive', 'time sensitive', 'cannot miss', 'must do', 'required'
        ]

        # Medium importance keywords
        medium_imp_words = [
            'review', 'follow up', 'reply', 'check', 'confirm', 'schedule',
            'prepare', 'organize', 'arrange', 'coordinate', 'plan'
        ]

        # Count occurrences
        high_count = sum(1 for word in high_imp_words if word in text)
        medium_count = sum(1 for word in medium_imp_words if word in text)

        # Calculate score based on keyword presence
        if high_count > 0:
            return min(0.8 + (high_count * 0.1), 1.0)  # Cap at 1.0
        elif medium_count > 0:
            return min(0.5 + (medium_count * 0.1), 0.8)
        else:
            return 0.3  # Default medium-low priority

    def _calculate_task_duration_score(self, task_details: Dict) -> float:
        """Calculate priority based on estimated task duration."""
        # For now, we'll assume shorter tasks might be prioritized higher
        # In a real system, this could be based on user input or ML predictions
        return 0.4  # Default medium priority

    def _calculate_user_history_score(self, task_details: Dict, user_context: Dict) -> float:
        """Calculate priority based on user's historical task completion patterns."""
        # In a real implementation, this would analyze the user's task history
        # to determine which types of tasks they tend to prioritize
        return 0.4  # Default medium priority

    def _calculate_recurrence_score(self, task_details: Dict, user_context: Dict) -> float:
        """Calculate priority based on recurrence pattern."""
        # In a real implementation, this would check if task is recurring
        # and how it was prioritized in the past
        return 0.4  # Default medium priority

    def _generate_reasoning(self, scores: Dict, task_details: Dict) -> str:
        """Generate human-readable explanation for the priority decision."""
        reasoning_parts = []

        if scores['deadline_proximity'] >= 0.7:
            due_date = task_details.get('due_date')
            if due_date:
                reasoning_parts.append(f"High priority due to upcoming deadline on {due_date}")

        if scores['keyword_importance'] >= 0.7:
            reasoning_parts.append("Contains high-importance keywords indicating urgency")

        if scores['task_duration'] >= 0.7:
            reasoning_parts.append("Short-duration task that can be completed quickly")

        if not reasoning_parts:
            reasoning_parts.append("Priority determined based on standard factors")

        return "; ".join(reasoning_parts)

    def suggest_smart_priority(self, title: str, description: str = "", due_date: str = None, user_context: Dict = None) -> Dict[str, any]:
        """
        Public method to suggest priority for a task based on its details.

        Args:
            title: Task title
            description: Task description
            due_date: Due date in ISO format
            user_context: Optional user context data

        Returns:
            Dict containing priority suggestion with confidence and reasoning
        """
        task_details = {
            'title': title,
            'description': description,
            'due_date': due_date
        }

        return self.calculate_priority(task_details, user_context)

    def _generate_reasoning(self, scores: Dict, task_details: Dict) -> str:
        """Generate human-readable explanation for the priority decision."""
        reasoning_parts = []

        if scores['deadline_proximity'] >= 0.7:
            due_date = task_details.get('due_date')
            if due_date:
                reasoning_parts.append(f"High priority due to upcoming deadline on {due_date}")

        if scores['keyword_importance'] >= 0.7:
            reasoning_parts.append("Contains high-importance keywords indicating urgency")

        if scores['task_duration'] >= 0.7:
            reasoning_parts.append("Short-duration task that can be completed quickly")

        if not reasoning_parts:
            reasoning_parts.append("Priority determined based on standard factors")

        return "; ".join(reasoning_parts)


# Global instance
priority_engine = PriorityEngine()


def suggest_smart_priority(title: str, description: str = "", due_date: str = None, user_context: Dict = None) -> Dict[str, any]:
    """
    Public function to suggest priority for a task.

    Args:
        title: Task title
        description: Task description
        due_date: Due date in ISO format
        user_context: Optional user context data

    Returns:
        Dict containing priority suggestion with confidence and reasoning
    """
    return priority_engine.suggest_smart_priority(title, description, due_date, user_context)