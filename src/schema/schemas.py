from typing import Optional

from pydantic import BaseModel, Field


class Dummy(BaseModel):
    """
    Pydantic model for 'Dummy' objects.

    This model is used for validating data related to Dummy objects in both requests and responses.

    Attributes:
        name (str): The name of the Dummy object, required, with a length constraint of 1-100 characters.
        description (str): A brief description of the Dummy object, required, with a length constraint of 1-100 characters.
        optional_field (Optional[str]): An optional field for additional information, can be either a string or None.
    """

    # The `id` field of type UUID is commented out to avoid conflict with the SQLAlchemy model.
    # id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    optional_field: Optional[str | None] = Field(default=None, max_length=100)


class DummyPatch(BaseModel):
    """
    Pydantic model for partial updates to 'Dummy' objects.

    This model is used when performing partial updates (PATCH requests) on Dummy objects.

    Attributes:
        name (Optional[str]): An optional field to update the name of the Dummy object.
        description (Optional[str]): An optional field to update the description of the Dummy object.
        optional_field (Optional[str]): An optional field for additional information that can be updated.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=100)
    optional_field: Optional[str | None] = Field(default=None, max_length=100)


class Token(BaseModel):
    """
    Pydantic model for JWT access token information.

    This model represents the structure of the JSON web token used for authenticated sessions.

    Attributes:
        access_token (str): The JWT access token string.
        token_type (str): The type of the token, typically 'bearer'.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Pydantic model for token payload data.

    Contains the information stored in the JWT token payload.

    Attributes:
        username (Optional[str]): The username contained in the token payload. It's optional and defaults to None.
    """

    username: str | None = None


class User(BaseModel):
    """
    Pydantic model for user information.

    This model is used for representing user data in various operations of the API.

    Attributes:
        username (str): The unique username of the user.
        email (Optional[str]): The email address of the user.
        full_name (Optional[str]): The full name of the user.
        disabled (Optional[bool]): Indicates whether the user account is disabled.
        password (str): The password of the user.
    """

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    password: str


class UserResponse(BaseModel):
    """
    Pydantic model for user information used in API responses.

    This model is specifically used for returning user data in API responses, excluding sensitive information like passwords.

    Attributes:
        username (str): The unique username of the user.
        email (str): The email address of the user.
        full_name (Optional[str]): The full name of the user.
        disabled (Optional[bool]): Indicates whether the user account is disabled.
    """

    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """
    Pydantic model for user information as stored in the database.

    Extends the User model with additional details specific to the database storage, like hashed passwords.

    Attributes:
        hashed_password (Optional[str]): The hashed password of the user.
    """

    hashed_password: str | None = None


class DisableUserRequest(BaseModel):
    """
    Pydantic model for disabling a user account.

    Used when a request is made to disable a user account, requiring the user's password for verification.

    Attributes:
        password (str): The password of the user, required for disabling the account.
    """

    password: str
