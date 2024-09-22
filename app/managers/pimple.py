from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Select, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Pimple


class PimpleManager:
    sql_model = Pimple

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, obj_uuid: UUID) -> Pimple:
        stmt = self._get_query().where(self.sql_model.uuid == obj_uuid)

        result = await self.session.scalar(stmt)

        if not result:
            raise ValueError(f"{self.sql_model.__name__} object with obj_uuid={str(obj_uuid)} not found")

        return result

    async def get_all(self) -> list[Pimple]:
        stmt = self._get_query()

        return (await self.session.scalars(stmt)).all()  # type: ignore

    async def create(self, obj: BaseModel) -> Pimple:
        stmt = insert(self.sql_model).values(**obj.model_dump(exclude_defaults=True)).returning(self.sql_model)

        return await self._apply_changes(stmt=stmt)

    async def update(self, obj: BaseModel, obj_uuid: UUID) -> Pimple:
        if not (updated_model := obj.model_dump(exclude_unset=True)):
            raise ValueError("No data provided for updating")

        stmt = (
            update(self.sql_model)
            .where(self.sql_model.uuid == obj_uuid)
            .values(**updated_model)
            .returning(self.sql_model)
        )

        return await self._apply_changes(stmt=stmt, obj_uuid=obj_uuid)

    def _get_query(self) -> Select:
        return select(self.sql_model)

    async def _apply_changes(
        self,
        stmt,
        obj_uuid: UUID | None = None,
    ) -> Pimple:
        try:
            result = await self.session.execute(stmt)

            result = result.scalar_one()

            await self.session.commit()

            return result

        except DBAPIError as exc:
            await self.session.rollback()
            raise exc

        except NoResultFound:
            raise ValueError(f"{self.sql_model.__name__} object with obj_uuid={str(obj_uuid)} not found")
