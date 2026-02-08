"""
Natural Language Processing module for task creation in the Todo Web Application.
Parses natural language input to extract task details like title, description, due date, priority, etc.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class NLPProcessor:
    """
    Natural Language Processor for extracting task details from user input.
    """

    def __init__(self):
        # Define patterns for extracting various components
        self.date_patterns = [
            r'today',
            r'tomorrow',
            r'next week',
            r'next month',
            r'in (\d+) (days?|hours?|weeks?|months?)',
            r'on (\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)',  # MM/DD/YYYY or DD/MM/YYYY
            r'on ([A-Za-z]+ \d{1,2}(?:st|nd|rd|th)?)',  # Month Day format
        ]

        self.priority_keywords = {
            'high': ['urgent', 'important', 'asap', 'critical', 'immediately', 'now', 'soon'],
            'medium': ['normal', 'standard', 'regular'],
            'low': ['later', 'when possible', 'eventually', 'whenever']
        }

        self.priority_factors = {
            'deadline_proximity': 0.35,
            'keyword_importance': 0.30,
            'task_duration': 0.10,
            'user_history': 0.15,
            'recurrence_pattern': 0.10
        }

        self.time_patterns = [
            r'at (\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)',
            r'at (\d{1,2}:\d{2})',
            r'by (\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)',
            r'by (\d{1,2}:\d{2})',
        ]

    def parse_task_from_natural_language(self, input_text: str) -> Dict[str, any]:
        """
        Parse natural language input to extract task components.

        Args:
            input_text: Natural language description of the task

        Returns:
            Dict containing parsed task components (title, description, due_date, priority, etc.)
        """
        try:
            logger.info(f"Parsing natural language task: {input_text}")

            # Extract task title (main action/verb phrase)
            title = self._extract_title(input_text)

            # Extract due date
            due_date = self._extract_due_date(input_text)

            # Extract priority based on keywords
            priority = self._extract_priority(input_text)

            # Extract description if available
            description = self._extract_description(input_text, title)

            # Extract tags/labels
            tags = self._extract_tags(input_text)

            result = {
                'title': title,
                'description': description,
                'due_date': due_date,
                'priority': priority,
                'tags': tags,
                'confidence': 0.8  # Default confidence score
            }

            logger.info(f"Parsed task: {result}")
            return result

        except Exception as e:
            logger.error(f"Error parsing natural language task: {str(e)}", exc_info=True)
            # Return a basic structure with the original text as title
            return {
                'title': input_text[:255],
                'description': '',
                'due_date': None,
                'priority': 'medium',
                'tags': [],
                'confidence': 0.0
            }

    def _extract_title(self, text: str) -> str:
        """Extract the main task title from natural language."""
        # Remove common prefixes/suffixes that don't contribute to the task
        text = re.sub(r'^(please|can you|would you|help me to?)\s*', '', text, flags=re.IGNORECASE)

        # Extract the main verb/action phrase
        # Look for imperative verbs or action phrases
        title_candidates = [
            re.search(r'(?:to\s+|to\s+be\s+|for\s+|about\s+)?(.+?)(?:\s+on\s+\w+|\s+at\s+\d+|\s+by\s+\d+|$)', text, re.IGNORECASE),
            re.search(r'(?:remind me to|tell me to|help me to|create|add|make|do)\s+(.+?)(?:\s+on\s+|\s+at\s+|\s+by\s+|$)', text, re.IGNORECASE),
        ]

        for candidate in title_candidates:
            if candidate:
                extracted = candidate.group(1).strip()
                if extracted:
                    # Capitalize the first letter
                    return extracted[0].upper() + extracted[1:] if len(extracted) > 1 else extracted.upper()

        # If no specific pattern matched, return the original text (first sentence)
        first_sentence = text.split('.')[0].split(',')[0].strip()
        return first_sentence[:255]  # Limit length

    def _extract_due_date(self, text: str) -> Optional[str]:
        """Extract due date from natural language text."""
        text_lower = text.lower()

        # Check for today/tomorrow
        if 'today' in text_lower:
            return datetime.now().strftime('%Y-%m-%d')
        elif 'tomorrow' in text_lower:
            return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        elif 'next week' in text_lower:
            return (datetime.now() + timedelta(weeks=1)).strftime('%Y-%m-%d')
        elif 'next month' in text_lower:
            return (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

        # Check for "in X days/hours/weeks/months"
        in_pattern = re.search(r'in (\d+) (day|hour|week|month)s?', text_lower)
        if in_pattern:
            num = int(in_pattern.group(1))
            unit = in_pattern.group(2)
            if 'day' in unit:
                return (datetime.now() + timedelta(days=num)).strftime('%Y-%m-%d')
            elif 'hour' in unit:
                return (datetime.now() + timedelta(hours=num)).strftime('%Y-%m-%d')
            elif 'week' in unit:
                return (datetime.now() + timedelta(weeks=num)).strftime('%Y-%m-%d')
            elif 'month' in unit:
                return (datetime.now() + timedelta(days=num*30)).strftime('%Y-%m-%d')

        # Check for specific date formats (MM/DD/YYYY, DD/MM/YYYY, Month Day)
        date_match = re.search(r'on (\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)', text)
        if date_match:
            date_str = date_match.group(1)
            # Convert to standard format
            try:
                if '/' in date_str:
                    parts = date_str.split('/')
                    if len(parts) == 3:
                        # Assume MM/DD/YYYY or DD/MM/YYYY - let's assume MM/DD/YYYY for now
                        month, day, year = parts
                        if len(year) == 2:
                            year = '20' + year
                        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    elif len(parts) == 2:
                        # MM/DD or DD/MM - let's assume MM/DD
                        month, day = parts
                        return f"{datetime.now().year}-{month.zfill(2)}-{day.zfill(2)}"
            except:
                pass

        # Check for Month Day format (e.g., "on January 15th")
        month_day_match = re.search(r'on ([A-Za-z]+ \d{1,2}(?:st|nd|rd|th)?)', text, re.IGNORECASE)
        if month_day_match:
            date_str = month_day_match.group(1)
            # Try to parse the date
            try:
                parsed_date = datetime.strptime(date_str.replace('th', '').replace('st', '').replace('nd', '').replace('rd', ''), '%B %d')
                # If month has already passed this year, assume next year
                current_date = datetime.now()
                if parsed_date.month < current_date.month or (parsed_date.month == current_date.month and parsed_date.day < current_date.day):
                    parsed_date = parsed_date.replace(year=current_date.year + 1)
                else:
                    parsed_date = parsed_date.replace(year=current_date.year)
                return parsed_date.strftime('%Y-%m-%d')
            except:
                pass

        return None

    def _extract_priority(self, text: str) -> str:
        """Extract priority based on keywords in the text."""
        text_lower = text.lower()

        # Check for high priority keywords
        for keyword in self.priority_keywords['high']:
            if keyword in text_lower:
                return 'high'

        # Check for low priority keywords
        for keyword in self.priority_keywords['low']:
            if keyword in text_lower:
                return 'low'

        # Default to medium priority
        return 'medium'

    def _extract_description(self, text: str, title: str) -> str:
        """Extract additional details as description."""
        # Remove the title from the text to get the remaining as description
        text_lower = text.lower()
        title_lower = title.lower()

        # Find the title in the text and get the remainder
        idx = text_lower.find(title_lower)
        if idx != -1:
            # Get text after the title
            desc_part = text[idx + len(title):].strip()
            if desc_part.startswith(('to', 'for', 'about')):
                desc_part = desc_part[desc_part.find(' ') + 1:].strip()
            return desc_part

        # If title wasn't found, return the original text without common prefixes
        clean_text = re.sub(r'^(please|can you|would you|help me to?)\s*', '', text, flags=re.IGNORECASE)
        return clean_text[len(title):].strip()

    def _extract_tags(self, text: str) -> list:
        """Extract tags/labels from the text."""
        # Look for hashtags or mentions of categories
        tags = []

        # Extract hashtags
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, text)
        tags.extend([tag.lower() for tag in hashtags])

        # Extract mentions (could represent people or groups)
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, text)
        tags.extend(['person:' + mention.lower() for mention in mentions])

        # Look for common categories based on keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['work', 'office', 'meeting', 'project']):
            tags.append('work')
        if any(word in text_lower for word in ['personal', 'home', 'family', 'private']):
            tags.append('personal')
        if any(word in text_lower for word in ['shopping', 'buy', 'grocery', 'purchase']):
            tags.append('shopping')

        return list(set(tags))  # Remove duplicates


# Global instance
nlp_processor = NLPProcessor()


def parse_task_from_natural_language(text: str) -> Dict[str, any]:
    """
    Public function to parse a task from natural language text.

    Args:
        text: Natural language description of the task

    Returns:
        Dict containing parsed task components
    """
    return nlp_processor.parse_task_from_natural_language(text)