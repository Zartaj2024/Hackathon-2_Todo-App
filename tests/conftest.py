import pytest
import os
import sys
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient

# Add phase_2/backend to sys.path to allow imports
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "phase_2", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Add phase_3/backend to sys.path
phase3_backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "phase_3", "backend"))
if phase3_backend_path not in sys.path:
    sys.path.insert(0, phase3_backend_path)

from main import app
from database import get_session

# Test database setup
sqlite_url = "sqlite:///./test.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    # Disable rate limiting for tests
    from main import limiter
    original_enabled = limiter.enabled
    limiter.enabled = False

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    limiter.enabled = original_enabled
