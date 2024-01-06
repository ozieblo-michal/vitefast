from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import auth.auth as auth
from schema.schemas import Token, User

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Generate an access token for authenticated users.

    This endpoint handles the user login process. Upon successful authentication, it returns a JWT access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data including the username and password.

    Returns:
        Token: A JWT token encapsulated within a Token schema.
    """
    return auth.login_for_access_token(form_data)

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    """Read and return the current authenticated user's information.

    This endpoint retrieves the information of the user who is currently authenticated using their access token.

    Args:
        current_user (User): The current authenticated user, obtained through dependency injection.

    Returns:
        User: The User schema containing the user's information.
    """
    return current_user

@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(auth.get_current_active_user)):
    """Get a list of items owned by the current authenticated user.

    This endpoint is a demonstration of how to access user-specific data,
    in this case, returning a list of dummy items owned by the user.

    Args:
        current_user (User): The current authenticated user, obtained through dependency injection.

    Returns:
        list: A list of dummy items with an item ID and the owner's username.
    """
    return [{"item_id": "Foo", "owner": current_user.username}]
