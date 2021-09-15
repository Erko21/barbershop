from app.serializers.auth import UserCreatedMsg, UserRegistration
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.services import AuthService
from app.serializers import User, Token
from app.dependecies import get_super_user, get_current_user, get_user

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserCreatedMsg)
async def sign_up(user_data: UserRegistration, user: User = Depends(get_user)):
    service = AuthService()
    return await service.register_new_user(user_data)


@router.post("/login", response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    service = AuthService()
    return await service.authenticate_user(form_data.username, form_data.password)


@router.get("/user", response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user


@router.post("/logout")
async def logout(user: User = Depends(get_current_user)):
    user.is_active = False
    return await user.save()
