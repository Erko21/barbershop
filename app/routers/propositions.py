from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends

from app.dependecies import get_user
from app.serializers import PropositionOut
from app.serializers.propositions import (
    PropositionCreatedMsg,
    PropositionCreation,
    PropositionDeletedMsg,
    PropositionToUpdate,
    PropositionUpdatedMsg,
)
from app.services.proposition import PropositionService
from app.models.user import User

router = APIRouter(prefix="/proposition")


@router.post("/create", response_model=PropositionCreatedMsg)
async def create_proposition(
    proposition: PropositionCreation, user: User = Depends(get_user)
):
    service = PropositionService()
    return await service.create_proposition(proposition)


@router.post("/delete_{pk}", response_model=PropositionDeletedMsg)
async def delete_proposition(pk: int, user: User = Depends(get_user)):
    service = PropositionService()
    return await service.delete(id=pk)


@router.post("/update_{pk}", response_model=PropositionUpdatedMsg)
async def update_proposition(
    pk: int, schema: PropositionToUpdate, user: User = Depends(get_user)
):
    service = PropositionService()
    return await service.update(schema, id=pk)


@router.get("/get_all", response_model=List[PropositionOut])
async def get_all_propositions():
    service = PropositionService()
    return await service.get_all()


@router.get("/get_one{pk}", response_model=PropositionOut)
async def get_one_proposition(pk: int):
    service = PropositionService()
    return await service.get(id=pk)


@router.get("/by_price_{price}", response_model=PropositionOut)
async def proposition_filtered_by_price(price: Decimal):
    service = PropositionService()
    return await service.filter(price=price)


@router.get("by_time_{time}", response_model=PropositionOut)
async def proposition_filtered_by_time(time: Decimal):
    service = PropositionService()
    return await service.filter(job_time=time)
