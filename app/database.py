import os
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "clinical_trials")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(expire_on_commit=False, bind=engine)
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()