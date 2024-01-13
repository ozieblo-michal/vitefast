import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import main

# Adding the directory containing the 'src' folder to sys.path.
# This allows modules within 'src' to be easily imported throughout the tests.
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


@pytest.fixture
def client():
    """
    Pytest fixture to create a TestClient instance for testing FastAPI endpoints.

    This fixture creates a client using FastAPI's TestClient, allowing HTTP requests to be made to the app for testing purposes.

    Returns:
        TestClient: A FastAPI TestClient instance with the application loaded for testing.
    """
    return TestClient(main.app)


def test_read_dummy(client):
    """
    Test the '/dummy' GET endpoint.

    This test checks if the '/dummy' endpoint responds with a status code of 200, indicating a successful response.

    Args:
        client (TestClient): The FastAPI TestClient instance used to make HTTP requests to the application.
    """
    response = client.get("/dummy")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"



def test_rate_limiter(client):
    for _ in range(5):
        response = client.get("/dummy")
        assert response.status_code in [200, 429]

    response = client.get("/dummy")
    assert response.status_code == 429
