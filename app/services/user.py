from typing import Optional
from fastapi.exceptions import HTTPException
from tortoise.query_utils import Q
from .base import BaseService

from services.auth import AuthService
from models.user import User
from serializers.auth import (
    UserCreatedMsg,
    UserRegistration,
    UserLogoutMsg,
)
from logger import log


class UserService(BaseService):
    model = User
    create_schema = UserRegistration

    async def get_username_email(self, username: str, email: str):
        return await self.model.get_or_none(Q(username=username) | Q(email=email))

    async def create_superuser(self, schema: UserRegistration):
        service = AuthService()
        hash_password = service.hash_password(schema.dict().pop("password"))
        return await self.create(
            UserRegistration(
                **schema.dict(exclude={"password"}),
                password=hash_password,
                is_active=True,
                is_superuser=True,
            )
        )
