import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.common import CommonMixin


class Pimple(CommonMixin, Base):
    description: Mapped[str] = mapped_column()
    number_of_presses: Mapped[int | None] = mapped_column(default=0)

    appeared_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )
    disappeared_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None,
    )
