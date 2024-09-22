from contextlib import asynccontextmanager
from typing import AsyncGenerator
from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import config, log

engine: AsyncEngine = create_async_engine(url=config.db.url)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[None, AsyncSession]:
    session = AsyncSessionLocal()
    try:
        yield session

    except SQLAlchemyError as exc:
        log.info("DB exception occurred, rolling back transaction", exception=str(exc))
        await session.rollback()

        raise exc

    finally:
        await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {
        UUID: PGUUID,
    }
