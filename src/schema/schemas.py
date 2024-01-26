from typing import Optional, Union

from pydantic import BaseModel, Field


class Dummy(BaseModel):
    """
    Pydantic model for validating input data for 'Dummy' objects.

    This model defines the structure and constraints for 'Dummy' data used in requests and responses.

    Attributes:
        name (str): The name of the Dummy object. Must be between 1 and 100 characters.
        description (str): The description of the Dummy object. Must be between 1 and 100 characters.
    """

    # The `id` field of type UUID is commented out to avoid conflict with the SQLAlchemy model.
    # id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    optional_field: Optional[Union[str, None]] = Field(default=None, max_length=100)


class DummyPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=100)
    optional_field: Optional[Union[str, None]] = Field(default=None, max_length=100)


class Token(BaseModel):
    """
    Pydantic model for access token information.

    Represents the structure of the JSON web token (JWT) used for authentication.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token, typically "bearer".
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Pydantic model for token payload data.

    Contains additional information that might be stored in the JWT token.

    Attributes:
        username (str, optional): The username contained in the token payload. Default is None.
    """

    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    password: str


class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str | None = None


class DisableUserRequest(BaseModel):
    password: str
