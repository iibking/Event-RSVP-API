from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from app.core.db_async import AsyncSessionLocal

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db