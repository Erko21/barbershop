from typing import TypeVar, Type, Optional

from fastapi import HTTPException
from pydantic import BaseModel
from tortoise import models
from app.logger import log


ModelType = TypeVar("ModelType", bound=models.Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)
QuerySchemaType = TypeVar("QuerySchemaType", bound=BaseModel)


class BaseService:
    model: Type[ModelType]
    create_schema: CreateSchemaType
    update_schema: UpdateSchemaType
    query_schema: QuerySchemaType
    get_schema: GetSchemaType

    async def create(self, schema, *args, **kwargs) -> Optional[CreateSchemaType]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        log(log.INFO, "Model %s has been created", self.model)
        res = await self.get_schema.from_tortoise_orm(obj)
        return res

    async def update(self, schema, **kwargs) -> Optional[UpdateSchemaType]:
        await self.model.filter(**kwargs).update(**schema.dict(exclude_unset=True))
        return await self.get_schema.from_queryset_single(self.model.get(**kwargs))

    async def delete(self, **kwargs):
        obj = await self.model.filter(**kwargs).delete()
        if not obj:
            raise HTTPException(status_code=404, detail="Object does not exist")

    async def get_all(self) -> Optional[GetSchemaType]:
        return await self.get_schema.from_queryset(self.model.all())

    async def filter(self, **kwargs) -> Optional[GetSchemaType]:
        return await self.get_schema.from_queryset(self.model.filter(**kwargs))

    async def get(self, **kwargs) -> Optional[GetSchemaType]:
        return await self.get_schema.from_queryset_single(self.model.get(**kwargs))

    async def get_obj(self, **kwargs) -> Optional[ModelType]:
        return await self.model.get_or_none(**kwargs)
