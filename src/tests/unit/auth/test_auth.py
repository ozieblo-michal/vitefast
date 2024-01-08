from fastapi.testclient import TestClient
import main
from jose import jwt
from schema.schemas import UserInDB
import auth.auth as auth

import db.fake_db as fake_db

db = fake_db.db

client = TestClient(main.app)

def test_create_access_token():
    user_data = {"sub": "testuser"}
    token = auth.create_access_token(user_data)
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    assert payload.get("sub") == user_data["sub"]

def test_authenticate_user():
    user = auth.authenticate_user(db, "testuser", "testpassword")
    assert user
    assert user.username == "testuser"

def test_get_current_user():
    user_data = {"sub": "testuser"}
    token = auth.create_access_token(user_data)
    current_user = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert current_user.status_code == 200
    assert current_user.json()["username"] == "testuser"

def test_get_current_active_user_inactive():
    user_data = {"sub": "inactive_user"}
    token = auth.create_access_token(user_data)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert "Inactive user" in response.text

def test_login_for_access_token():
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
