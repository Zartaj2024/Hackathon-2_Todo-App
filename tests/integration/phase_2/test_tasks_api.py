import pytest
import os
import sys
from sqlmodel import Session, select
from fastapi import status

from jose import jwt
from config import settings

# Fixture for creating a test user and returning its token
@pytest.fixture
def test_user_info(client):
    user_data = {
        "email": "integration@test.com",
        "password": "Password123!",
        "name": "Integration Test"
    }
    client.post("/api/v1/register", json=user_data)
    response = client.post("/api/v1/login", json={"email": user_data["email"], "password": user_data["password"]})
    token = response.json()["access_token"]

    # Decode token to get user_id (sub)
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    user_id = payload.get("sub")

    return {"token": token, "user_id": user_id}

def test_create_task_integration(client, test_user_info):
    task_data = {
        "title": "Integration Task",
        "description": "Testing integration",
        "user_id": test_user_info["user_id"]
    }
    response = client.post(
        "/api/v1/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {test_user_info['token']}"}
    )

    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]
    data = response.json()
    assert data["title"] == "Integration Task"
    assert "id" in data

def test_get_tasks_integration(client, test_user_info):
    # Create a task first
    client.post(
        "/api/v1/tasks/",
        json={"title": "Task 1", "user_id": test_user_info["user_id"]},
        headers={"Authorization": f"Bearer {test_user_info['token']}"}
    )

    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {test_user_info['token']}"}
    )

    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert len(tasks) >= 1
    assert any(t["title"] == "Task 1" for t in tasks)

def test_unauthorized_access(client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
