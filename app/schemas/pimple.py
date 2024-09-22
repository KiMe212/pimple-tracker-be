from datetime import datetime
from uuid import UUID

from pydantic import NonNegativeInt

from app.schemas.base import BaseSchema


class CreatePimpleSchema(BaseSchema):
    description: str
    number_of_presses: NonNegativeInt


class PimpleSchema(CreatePimpleSchema):
    uuid: UUID
    appeared_at: datetime
    disappeared_at: datetime | None


class ListPimpleSchema(BaseSchema):
    items: list[PimpleSchema]


class UpdatePimpleSchema(BaseSchema):
    description: str | None = None
    number_of_presses: NonNegativeInt | None = None


class DeletePimpleSchema(BaseSchema):
    disappeared_at: datetime | None = None
