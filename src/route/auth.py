from fastapi import Depends, APIRouter

router = APIRouter()

import auth.auth as auth
from fastapi.security import OAuth2PasswordRequestForm 
from schema.schemas import Token, User


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print('dupa jasia')
    return auth.login_for_access_token(form_data)

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user

@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(auth.get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

