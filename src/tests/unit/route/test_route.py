import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import main

# Dodanie katalogu zawierającego folder 'src' do sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


@pytest.fixture
def client():
    return TestClient(main.app)


def test_read_dummy(client):
    response = client.get("/dummy")
    assert response.status_code == 200
