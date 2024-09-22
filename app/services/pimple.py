from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import db_session_dependency
from app.managers import PimpleManager
from app.schemas import CreatePimpleSchema, DeletePimpleSchema, ListPimpleSchema, PimpleSchema, UpdatePimpleSchema


class PimpleService:
    schema = PimpleSchema
    list_schema = ListPimpleSchema

    def __init__(self, db_session: Annotated[AsyncSession, Depends(db_session_dependency)]):
        self.db_session = db_session
        self.manager = PimpleManager(db_session)

    async def get(self, obj_uuid: Any) -> PimpleSchema:
        result = await self.manager.get(obj_uuid=self._check_obj_uuid(obj_uuid))

        return self.schema.model_validate(result)

    async def get_all(self) -> ListPimpleSchema:
        result = await self.manager.get_all()

        return self.list_schema.model_validate({"items": result})

    async def create(self, obj: CreatePimpleSchema) -> PimpleSchema:
        result = await self.manager.create(obj=obj)

        return self.schema.model_validate(result)

    async def update(self, obj: UpdatePimpleSchema, obj_uuid: Any) -> PimpleSchema:
        result = await self.manager.update(obj=obj, obj_uuid=self._check_obj_uuid(obj_uuid))

        return self.schema.model_validate(result)

    @classmethod
    def _check_obj_uuid(cls, obj_uuid: Any) -> UUID:
        try:
            return UUID(str(obj_uuid))
        except ValueError:
            raise ValueError("`obj_uuid` must be a valid UUID")

    async def delete(self, obj: DeletePimpleSchema, obj_uuid: Any) -> None:
        _ = await self.manager.update(obj=obj, obj_uuid=self._check_obj_uuid(obj_uuid))
