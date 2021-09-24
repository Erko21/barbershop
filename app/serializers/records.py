from tortoise import Tortoise
from tortoise.contrib.pydantic.base import PydanticModel
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Record


Tortoise.init_models(["app.models"], "models")

Record_Get_Pydantic = pydantic_model_creator(
    Record,
)


class BaseRecord(BaseModel):
    id: int


class RecordOut(PydanticModel):
    id: int
    customer_email: EmailStr
    customer_phone_number: str
    customer_full_name: str
    time: datetime
    user_id: int
    proposition_id: int


class RecordCreation(BaseModel):
    customer_email: EmailStr
    customer_phone_number: str
    customer_full_name: str
    time: datetime
    proposition_id: int
    user_id: int


class RecordCreated(BaseModel):
    id: int
    customer_full_name: str
    time: datetime
    user_id: int


class RecordUpdatedMsg(BaseModel):
    status: str = "OK"
    detail: str = "Proposition has been updated successfully"
    customer_full_name: str


class RecordToUpdate(BaseModel):
    customer_email: Optional[EmailStr]
    customer_phone_number: Optional[str]
    customer_full_name: Optional[str]
    time: Optional[datetime]
    proposition: Optional[int]
    user: Optional[int]
