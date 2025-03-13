from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config.settings import DATABASE_URL

class Base(DeclarativeBase):
    pass



engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    """Создание таблиц при первом запуске."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
