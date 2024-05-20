from datetime import datetime, timedelta
from pprint import pprint

import pytest
from fastapi.testclient import TestClient

from app.controllers.api.v1.root import app  # Import your FastAPI application


@pytest.fixture(scope="module")  # Create a test client once for all tests
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_root_status_code_200(client):
    """GET to ~/apiv1/root should return 200"""
    # client = TestClient(app)  # Create a test client
    response = client.get("/")  # Simulate a GET request to the root path
    print(f"\nRESPONSE: {response}\n")
    assert response.status_code == 200  # Check if the response is successful (200 OK)


def test_root_under_construction(client):
    # client = TestClient(app)  # Create a test client
    response = client.get("/")  # Simulate a GET request to the root path
    assert (
        "<h2>Under Construction</h2>" in response.text
    )  # Check if specific content is present


def test_get_status_success(client):
    """Test that the /status endpoint returns a successful status."""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    pprint(data)
    assert data["status"] == "ok"
    assert data["database"] == "connected"
    assert data["dependencies"]["database"]["version"] == "16.3"
    assert data["dependencies"]["database"]["max_connections"] == 100
    assert data["dependencies"]["database"]["opened_connections"] == 1

    # Validate 'updated_at' timestamp is recent (within a minute)
    updated_at = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
    assert datetime.now() - updated_at < timedelta(minutes=1)
