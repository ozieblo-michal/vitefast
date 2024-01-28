import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import main


from model.models import Dummy, Base


from db.dependencies import get_db


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import StaticPool

# Adding the directory containing the 'src' folder to sys.path.
# This allows modules within 'src' to be easily imported throughout the tests.
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

client = TestClient(main.app)


@pytest.fixture(scope="module")
def test_db():
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    main.app.dependency_overrides[get_db] = lambda: SessionLocal()

    try:
        db = SessionLocal()
        item = Dummy(
            name="item1",
            description="dummy description",
            optional_field="optional text",
        )
        db.add(item)
        db.commit()
        yield db
    finally:
        db.close()


def test_read_dummy(test_db):
    """
    Test the '/dummy' GET endpoint.

    This test checks if the '/dummy' endpoint responds with a status code of 200, indicating
    a successful response.

    Args:
        client (TestClient): The FastAPI TestClient instance used to make HTTP requests to
                             the application.
    """

    response = client.get("/dummy")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_rate_limiter(test_db):
    for _ in range(5):
        response = client.get("/dummy")
        assert response.status_code in [200, 429]

    response = client.get("/dummy")
    assert response.status_code == 429
