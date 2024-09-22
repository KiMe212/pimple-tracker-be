import datetime
from typing import Optional
from uuid import UUID

from pydantic.alias_generators import to_snake
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declarative_mixin, declared_attr, mapped_column


@declarative_mixin
class CommonMixin:
    repr_cols: tuple[str] | tuple[str, ...] = ("uuid",)

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=func.gen_random_uuid())

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.current_timestamp(),
        server_onupdate=func.current_timestamp(),
    )

    @declared_attr
    def __tablename__(cls):
        return to_snake(cls.__name__)  # type: ignore

    def __repr__(self) -> str:
        """
        Don't add relationships to the `repr_cols`, because they may lead to unexpected loading
        """
        return f"<{self.__class__.__name__} {', '.join([f'{col}={getattr(self, col)}' for col in self.repr_cols])}>"
