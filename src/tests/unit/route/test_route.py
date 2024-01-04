from fastapi.testclient import TestClient
from src import main
import pytest



@pytest.fixture
def client():
    return TestClient(main)

def test_read_dummy(client):
    response = client.get("/dummy")
    assert response.status_code == 200
