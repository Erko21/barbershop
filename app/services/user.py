from app.serializers.auth import User_Get_Pydantic
from typing import Optional
from tortoise.query_utils import Q
from fastapi import HTTPException, status

from app.services import BaseService, AuthService
from app.models import User as UserModel
from app.serializers import (
    UserRegistration,
)
from app.logger import log
from app.serializers import User, Token, UserInDb


class UserService(BaseService):
    model = UserModel
    create_schema = UserRegistration
    update_schema = UserInDb
    get_schema = User_Get_Pydantic

    async def get_username_email(self, username: str, email: str):
        return await self.model.get_or_none(Q(username=username) | Q(email=email))

    async def create_superuser(self, schema: UserRegistration):
        service = AuthService()
        hash_password = service.hash_password(schema.dict().pop("password"))
        return await self.create(
            UserRegistration(
                **schema.dict(exclude={"password"}),
                password=hash_password,
                is_superuser=True,
            )
        )

    async def register_new_user(self, user_data: UserRegistration) -> User:
        user = await UserModel.create(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            hash_password=AuthService.hash_password(user_data.password),
        )
        log(log.INFO, "User %s has been created", user_data.username)
        return user

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        def exception():
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await self.model.get(username=username)
        auth = AuthService()

        if user:
            await self.update(schema=UserInDb(is_active=True), id=user.id)
        if not user:
            log(log.ERROR, "User %s does not exist", username)
            raise exception()

        if not auth.verify_password(password, user.hash_password):
            log(log.ERROR, "Password is not correct")
            raise exception()

        log(log.INFO, "User has been logged")
        return auth.create_token(user)
