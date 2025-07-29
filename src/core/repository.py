from typing import Any, TypeVar
from uuid import UUID

from essentials.exceptions import ObjectNotFound
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.core.db import Base
from src.core.schemas import BaseStruct


TModel = TypeVar("TModel", bound=DeclarativeBase)
TSchema = TypeVar("TSchema", bound=BaseStruct)

TModelId = UUID | int


class BaseSQLAlchemyRepository[TModel]:
    def __init__(self, model: type[TModel], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, pk: TModelId, **filters: Any) -> TModel:
        stmt = select(self.model).where(self.model.id == pk)
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        obj = (await self.session.scalars(stmt)).first()
        if not obj:
            raise ObjectNotFound(f"{self.model.__name__} with id {pk} not found.")
        return obj

    async def list(self, **filters: Any) -> list[TModel]:
        stmt = select(self.model)
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        return (await self.session.scalars(stmt)).unique().all()

    async def create(self, instance: TModel | TSchema, **kwargs: Any) -> TModel:
        if isinstance(instance, BaseStruct):
            instance = instance.to_model(self.model, **kwargs)

        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: TModel | TSchema, pk: TModelId, **filters: Any) -> TModel:
        existing_instance = await self.get(pk, **filters)
        for key, value in instance.to_dict().items():
            setattr(existing_instance, key, value)
        await self.session.commit()
        await self.session.refresh(existing_instance)
        return existing_instance

    async def delete(self, pk: TModelId, **filters: Any) -> None:
        instance = await self.get(pk, **filters)
        await self.session.delete(instance)
        await self.session.commit()
