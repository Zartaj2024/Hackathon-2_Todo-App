import requests
import json

# Test the backend API
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_ready_endpoint():
    """Test the readiness endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/ready")
        print(f"Readiness check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Readiness check failed: {e}")
        return False

def test_docs_endpoint():
    """Test the documentation endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Docs endpoint: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Docs endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Todo App Backend API...")
    print("="*40)

    test_health_endpoint()
    print("-" * 20)
    test_ready_endpoint()
    print("-" * 20)
    test_docs_endpoint()

    print("="*40)
    print("Testing completed!")