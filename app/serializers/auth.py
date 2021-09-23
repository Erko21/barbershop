from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import User, Role


User_Get_Pydantic = pydantic_model_creator(
    User,
)


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    is_active: bool
    role: str


class UserCredentials(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreatedMsg(BaseModel):
    status: str = "OK"
    detail: str = "User has been created successfully"
    id: int


class UserLogoutMsg(BaseModel):
    status: str = "OK"
    detail: str = "User has been logged out successfully"


class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = Role.BARBER
    password: str


class UserInDb(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: str = Role.BARBER
    password: Optional[str] = None
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
