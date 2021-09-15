from services import AuthService
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.serializers import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


async def get_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_super_user(super_user: User = Depends(get_user)):
    if not super_user.role == "Admin":
        raise HTTPException(status_code=400, detail="You are not superuser")
    return super_user
