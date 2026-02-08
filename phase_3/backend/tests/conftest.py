import pytest
import os
import sys
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

# Add phase_2 and phase_3 paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "phase_2", "backend")))

from main import app
import auth_enhanced
from chat_api import chat

@pytest.fixture(autouse=True)
def mock_auth():
    """Fixture to override authentication dependency automatically for all Phase 3 tests."""
    mock_user = MagicMock()
    mock_user.id = "test-user-id"
    mock_user.email = "test@example.com"
    mock_user.name = "Test User"
    
    # Override both get_current_user and get_current_user_id
    app.dependency_overrides[auth_enhanced.get_current_user] = lambda: mock_user
    app.dependency_overrides[auth_enhanced.get_current_user_id] = lambda: mock_user.id
    app.dependency_overrides[chat.get_current_user] = lambda: mock_user
    app.dependency_overrides[chat.get_current_user_id] = lambda: mock_user.id
    
    yield mock_user
    app.dependency_overrides.clear()
