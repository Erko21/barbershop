from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.services.user import UserService
from app.serializers import User, Token
from app.dependecies import get_superuser, get_current_user, get_user
from app.serializers.auth import UserCreatedMsg, UserRegistration, UserLogoutMsg

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=UserCreatedMsg)
# async def sign_up(user_data: UserRegistration, user: User = Depends(get_superuser)):
async def sign_up(user_data: UserRegistration):
    service = UserService()
    return await service.register_new_user(user_data)


@router.post("/login", response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    service = UserService()
    return await service.authenticate_user(form_data.username, form_data.password)


@router.get("/user", response_model=User)
async def get_user(pk: int, user: User = Depends(get_user)):
    service = UserService()
    return await service.get(id=pk)


@router.get("/all", response_model=List[User])
async def get_all_user(user: User = Depends(get_user)):
    user_service = UserService()
    return user_service.get_all()


@router.post("/logout", response_model=UserLogoutMsg)
async def logout(user: User = Depends(get_user)):
    user.is_active = False
    return await user.save()
