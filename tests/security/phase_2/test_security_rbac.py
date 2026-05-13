import pytest
from fastapi import status
from jose import jwt
from config import settings
from datetime import datetime, timedelta
import uuid

@pytest.fixture
def user1_info(client):
    uid = str(uuid.uuid4())[:8]
    user_data = {"email": f"user1_{uid}@security.com", "password": "Password123!", "name": "User One"}
    client.post("/api/v1/register", json=user_data)
    response = client.post("/api/v1/login", json={"email": user_data["email"], "password": user_data["password"]})
    token = response.json()["access_token"]
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return {"token": token, "user_id": payload.get("sub")}

@pytest.fixture
def user2_info(client):
    uid = str(uuid.uuid4())[:8]
    user_data = {"email": f"user2_{uid}@security.com", "password": "Password123!", "name": "User Two"}
    client.post("/api/v1/register", json=user_data)
    response = client.post("/api/v1/login", json={"email": user_data["email"], "password": user_data["password"]})
    token = response.json()["access_token"]
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return {"token": token, "user_id": payload.get("sub")}

def test_unauthorized_task_access(client, user1_info, user2_info):
    # User 1 creates a task
    task_data = {"title": "User 1 Task", "user_id": user1_info["user_id"]}
    resp = client.post(
        "/api/v1/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {user1_info['token']}"}
    )
    task_id = resp.json()["id"]

    # User 2 tries to access User 1's task
    resp = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_info['token']}"}
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_unauthorized_task_delete(client, user1_info, user2_info):
    # User 1 creates a task
    task_data = {"title": "User 1 Task to Delete", "user_id": user1_info["user_id"]}
    resp = client.post(
        "/api/v1/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {user1_info['token']}"}
    )
    task_id = resp.json()["id"]

    # User 2 tries to delete User 1's task
    resp = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_info['token']}"}
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_expired_token(client):
    # Manually create an expired token
    expire = datetime.utcnow() - timedelta(minutes=1)
    to_encode = {"sub": "some-user-id", "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {encoded_jwt}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
