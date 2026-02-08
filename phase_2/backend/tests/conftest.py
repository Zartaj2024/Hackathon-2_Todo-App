"""
Configuration for pytest in the AI chatbot tests.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path so tests can import modules
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Set environment variables if needed
os.environ.setdefault("TESTING", "True")