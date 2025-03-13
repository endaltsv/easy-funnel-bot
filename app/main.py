import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.config.settings import BOT_TOKEN
from app.core.database import init_db
from app.routers import funnel_setup, join_request, broadcast


async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(funnel_setup.router)
    dp.include_router(join_request.router)
    # dp.include_router(broadcast.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
