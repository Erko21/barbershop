from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends

from app.dependecies import get_user
from app.serializers import PropositionOut
from app.serializers.propositions import (
    PropositionCreated,
    PropositionCreation,
    PropositionToUpdate,
    PropositionUpdatedMsg,
)
from app.services.proposition import PropositionService
from app.models.user import User

router = APIRouter(prefix="/propositions", tags=["Proposition"])


@router.post("/create", response_model=PropositionCreated)
async def create_proposition(
    proposition: PropositionCreation, user: User = Depends(get_user)
):
    service = PropositionService()
    return await service.create_proposition(proposition)


@router.post("/delete", status_code=204)
async def delete_proposition(pk: int, user: User = Depends(get_user)):
    service = PropositionService()
    return await service.delete(id=pk)


@router.post("/update", response_model=PropositionUpdatedMsg)
async def update_proposition(
    pk: int, schema: PropositionToUpdate, user: User = Depends(get_user)
):
    service = PropositionService()
    return await service.update(schema, id=pk)


@router.get("/get_all", response_model=List[PropositionOut])
async def get_all_propositions():
    service = PropositionService()
    return await service.get_all()


@router.get("/by_price", response_model=List[PropositionOut])
async def proposition_filtered_by_price(price: Decimal):
    service = PropositionService()
    return await service.filter(price=price)


@router.get("/by_time", response_model=List[PropositionOut])
async def proposition_filtered_by_time(time: Decimal):
    service = PropositionService()
    return await service.filter(job_time=time)


@router.get("/{pk}", response_model=PropositionOut)
async def get_proposition(pk: int):
    service = PropositionService()
    return await service.get(id=pk)
