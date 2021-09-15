from pydantic import BaseModel
from pydantic.networks import EmailStr


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


class UserLogoutMsg(BaseModel):
    status: str = "OK"
    detail: str = "User has been logged out successfully"


class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str
    password: str
