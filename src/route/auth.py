from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import auth.auth as auth
from schema.schemas import Token, User, UserInDB, DisableUserRequest, UserResponse

import service.services as service



from sqlalchemy.orm import Session
from route.routes import get_db

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




from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    if password is None:
        raise ValueError("Password cannot be None")
    return pwd_context.hash(password)



@router.post("/users/", response_model=UserResponse)
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_in_db = UserInDB(**user.dict(), hashed_password=hash_password(user.password))
    return service.create_user(db=db, user=user_in_db)







@router.patch("/users/{username}/disable", response_model=User)
def disable_user(username: str, disable_request: DisableUserRequest, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth.verify_password(disable_request.password, db_user.hashed_password):
        raise HTTPException(status_code=403, detail="Incorrect password")

    db_user.disabled = True
    db.commit()
    return db_user





# add get by ID