from fastapi.testclient import TestClient

from app.controllers.api.v1.root import app  # Import your FastAPI application


def test_root_status_code_200():
    client = TestClient(app)  # Create a test client
    response = client.get("/")  # Simulate a GET request to the root path
    assert response.status_code == 200  # Check if the response is successful (200 OK)


def test_root_under_construction():
    client = TestClient(app)  # Create a test client
    response = client.get("/")  # Simulate a GET request to the root path
    assert (
        "<h2>Under Construction</h2>" in response.text
    )  # Check if specific content is present
