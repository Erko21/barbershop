from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Proposition

User_Get_Pydantic = pydantic_model_creator(
    Proposition,
)


class BaseProposition(BaseModel):
    proposition_name: str


class PropositionOut(BaseProposition):
    price: Decimal
    job_time: Decimal


class PropositionCreation(BaseModel):
    proposition_name: str
    job_time: Decimal
    price: Decimal


class PropositionCreatedMsg(BaseModel):
    status: str = "OK"
    detail: str = "Proposition has been created successfully"


class PropositionDeletedMsg(BaseModel):
    status: str = "OK"
    detail: str = "Proposition has been deleted successfully"


class PropositionUpdatedMsg(BaseModel):
    status: str = "OK"
    detail: str = "Proposition has been updated successfully"


class PropositionToUpdate(BaseModel):
    proposition_name: Optional[str]
    job_time: Optional[Decimal]
    price: Optional[Decimal]
