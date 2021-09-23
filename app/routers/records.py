from datetime import datetime
from app.models.user import User
from app import routers, services
from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends

from app.services import RecordService
from app.dependecies import get_user
from app.serializers.records import (
    BaseRecord,
    RecordUpdatedMsg,
    Record_Get_Pydantic,
    RecordCreated,
    RecordCreation,
    RecordOut,
    RecordToUpdate,
)


router = APIRouter(prefix="/record", tags=["Record"])


@router.post("/create", response_model=RecordOut)
async def record_create(record: RecordCreation):
    service = RecordService
    return await service.create_record(record)


@router.post("/delete", status_code=204)
async def delete_record(pk: int, user: User = Depends(get_user)):
    service = RecordService
    return await service.delete(id=pk)


@router.post("/update", response_model=RecordUpdatedMsg)
async def update_record(
    pk: int, schema: RecordToUpdate, user: User = Depends(get_user)
):
    service = RecordService
    return await service.update(schema, id=pk)


@router.get("/all", response_model=List[RecordOut])
async def get_records():
    service = RecordService
    return await service.get_all()


@router.get("/get_record", response_model=RecordOut)
async def get_record(pk: int, user: User = Depends(get_user)):
    service = RecordService
    return await service.get(id=pk)


@router.get("/by_date", response_model=List[RecordOut])
async def record_filtered_by_price(date: datetime, user: User = Depends(get_user)):
    service = RecordService
    return await service.filter(time=date)
