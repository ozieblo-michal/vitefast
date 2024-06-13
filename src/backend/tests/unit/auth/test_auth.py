from fastapi.testclient import TestClient
from jose import jwt
import auth.auth as auth
import main
from db.dependencies import get_db
from auth.utils import get_password_hash
from model.models import User, Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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

        user = User(
            username="testuser",
            full_name="testuser",
            email="testmail",
            password=get_password_hash("testpassword"),
        )

        db.add(user)
        db.commit()

        user = User(
            username="testuser_disabled",
            full_name="testuser",
            email="testmail_disabled",
            password=get_password_hash("testpassword"),
            disabled=True,
        )

        db.add(user)
        db.commit()

        yield db
    finally:
        db.close()
        # Base.metadata.drop_all(bind=test_engine)


def test_create_access_token():
    user_data = {"sub": "testuser"}
    token = auth.create_access_token(user_data)
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    assert payload.get("sub") == user_data["sub"]


def test_authenticate_user(test_db):
    user = auth.authenticate_user("testuser", "testpassword", test_db)

    assert user.username == "testuser"


def test_get_current_user(test_db):
    user_data = {"sub": "testuser"}

    token = auth.create_access_token(user_data)

    current_user = client.get(
        "auth/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert current_user.status_code == 200
    assert current_user.json()["username"] == "testuser"


def test_get_current_active_user_inactive():
    user_data = {"sub": "testuser_disabled"}

    token = auth.create_access_token(user_data)

    response = client.get("auth/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert "Inactive user" in response.text


def test_login_for_access_token():
    login_data = {"username": "testuser", "password": "testpassword"}

    response = client.post("auth/token", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
