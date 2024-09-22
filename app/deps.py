from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session


async def db_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async with get_db_session() as session:
        yield session
