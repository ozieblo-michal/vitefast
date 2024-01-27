from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import auth.utils as utils

# from db.fake_db import db
from schema.schemas import TokenData, User, UserInDB, UserResponse


import model.models as models


from sqlalchemy.orm import Session

# openssl rand -hex 32
SECRET_KEY = "e69df904acecb0f9420801b460fc1f85f774b418df3eb3d18906736d5ecd23ae"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# todo, redundant with routes
from db.database import SessionLocal


def get_db():
    """Dependency function to obtain a database session.

    This function yields a SQLAlchemy session from a session factory upon request and closes it after use.

    Yields:
        Session: A SQLAlchemy session object to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nie można zweryfikować poświadczeń",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Setting up OAuth2 with Password (and Bearer) as the authentication method.
# The tokenUrl parameter indicates the URL where the client can get the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to verify the password input against the stored hashed password.
# Returns True if the password matches, ensuring secure password verification.
def verify_password(plain_password, hashed_password):
    """Verify a plain password against the hashed version.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return utils.pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, username: str) -> User | None:
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        return User(**db_user.__dict__)
    return None


# Function to authenticate the user by verifying the username and password.
# Returns the user object if authentication is successful, otherwise False.
def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user by username and password.

    Args:
        db (dict): The database representation (usually a dictionary).
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        User or False: The authenticated user object, or False if authentication fails.
    """

    user = get_user(db, username)

    if not user or not verify_password(password, user.password):
        return False
    return UserResponse(**user.__dict__)


# Function to create a JWT access token with an optional expiry.
# Encodes user-related data (like username) into a token for secure transmission.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token for a user.

    Args:
        data (dict): The payload data to be included in the token.
        expires_delta (timedelta, optional): The expiry time for the token. Defaults to 15 minutes.

    Returns:
        str: A JWT encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency function to get the current user from the token.
# Throws an error if the token is invalid, ensuring secure access to user-specific endpoints.
async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """Get the current user from the provided token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        User: The user associated with the token.

    Raises:
        HTTPException: 401 error if the token is invalid or the user is not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception()
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception()
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception()
    return user


# Dependency function to get the current active user.
# Throws an error if the user is disabled, ensuring only active users can access certain endpoints.
async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user),
):
    """Get the current active user.

    Args:
        current_user (User): The user to check for activity.

    Returns:
        User: The active user.

    Raises:
        HTTPException: 400 error if the user is inactive.
    """

    user = current_user
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


# Endpoint to handle login and return an access token.
# Validates user credentials and returns a JWT token for authenticated sessions.
def login_for_access_token(
    db: Session, form_data: OAuth2PasswordRequestForm = Depends()
):
    """Authenticate and return an access token for a valid user.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
        dict: Access token and token type.

    Raises:
        HTTPException: 401 error if the user cannot be authenticated.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
