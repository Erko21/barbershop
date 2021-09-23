from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Proposition

Proposition_Get_Pydantic = pydantic_model_creator(
    Proposition,
)


class BaseProposition(BaseModel):
    name: str


class PropositionOut(BaseProposition):
    id: int
    price: Decimal
    job_time: Decimal


class PropositionCreation(BaseModel):
    name: str
    job_time: Decimal
    price: Decimal


class PropositionCreated(BaseModel):
    id: int
    price: Decimal
    job_time: Decimal


class PropositionUpdatedMsg(BaseModel):
    status: str = "OK"
    detail: str = "Proposition has been updated successfully"
    price: Decimal


class PropositionToUpdate(BaseModel):
    name: Optional[str]
    job_time: Optional[Decimal]
    price: Optional[Decimal]


class PropositionInfo(BaseModel):
    id: int
    name: str
    job_time: Decimal
    price: Decimal
