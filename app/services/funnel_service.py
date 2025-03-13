from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.funnel import Funnel


async def get_funnel(channel_id: str) -> Funnel | None:
    async with SessionLocal() as session:
        result = await session.execute(select(Funnel).where(Funnel.channel_id == channel_id))
        return result.scalar()


async def upsert_funnel(channel_id: str, text: str, button_type: str | None,
                        button_text: str | None, button_url: str | None):
    async with SessionLocal() as session:
        funnel = await session.scalar(
            select(Funnel).where(Funnel.channel_id == channel_id)
        )
        if funnel is None:
            funnel = Funnel(
                channel_id=channel_id,
                text=text,
                button_type=button_type,
                button_text=button_text,
                button_url=button_url
            )
            session.add(funnel)
        else:
            funnel.text = text
            funnel.button_type = button_type
            funnel.button_text = button_text
            funnel.button_url = button_url
        await session.commit()
