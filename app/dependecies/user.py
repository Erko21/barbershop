from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends

from app.serializers import User
from app.services import AuthService
from app.schemas import oauth2_scheme


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


async def get_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_all_user(user: User):
    pass


async def get_superuser(superuser: User = Depends(get_user)):
    if not superuser.role == "Admin":
        raise HTTPException(status_code=400, detail="You are not superuser")
    return superuser
