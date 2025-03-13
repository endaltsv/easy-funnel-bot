from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.user import User

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


async def save_user(tg_user_id: int, username: str, channel_id: str):
    """
    Сохраняет пользователя (если ещё нет) в базу, привязанного к каналу.
    """
    try:
        async with SessionLocal() as session:
            existing_user = await session.scalar(
                select(User).where(User.tg_user_id == tg_user_id, User.channel_id == channel_id)
            )
            if existing_user:
                return  # Такой пользователь уже записан для этого канала

            new_user = User(
                tg_user_id=tg_user_id,
                username=username or "",
                channel_id=channel_id
            )
            session.add(new_user)
            await session.commit()

    except SQLAlchemyError as e:
        print(f"[DB ERROR] Ошибка при сохранении пользователя: {e}")


async def get_users_by_channel(channel_id: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.channel_id == channel_id)
        )
        return result.scalars().all()
