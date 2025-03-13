# import logging
# from aiogram import Router, F
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message
# from aiogram.filters import Command
# from aiogram.enums import ParseMode
#
# from app.services.user_service import get_users_by_channel
# from app.core.bot import bot
#
# router = Router()
#
#
# class BroadcastStates(StatesGroup):
#     waiting_for_channel = State()
#     waiting_for_text = State()
#
#
# @router.message(Command(commands="send_broadcast"))
# async def cmd_send_broadcast(message: Message, state: FSMContext):
#     await state.set_state(BroadcastStates.waiting_for_channel)
#     await message.answer("Введите channel_id (или @username), по которому делаем рассылку:")
#
#
# @router.message(BroadcastStates.waiting_for_channel)
# async def ask_broadcast_channel(message: Message, state: FSMContext):
#     channel_id = message.text.strip()
#     await state.update_data(channel_id=channel_id)
#     await state.set_state(BroadcastStates.waiting_for_text)
#     await message.answer("Теперь отправьте текст для рассылки:")
#
#
# @router.message(BroadcastStates.waiting_for_text)
# async def do_broadcast(message: Message, state: FSMContext):
#     text = message.text
#     data = await state.get_data()
#     channel_id = data["channel_id"]
#
#     users = await get_users_by_channel(channel_id)
#
#     await message.answer(f"Начинаю рассылку по каналу <b>{channel_id}</b>, пользователей: {len(users)}",
#                          parse_mode=ParseMode.HTML)
#
#     sent, failed = 0, 0
#     for user in users:
#         try:
#             await bot.send_message(user.tg_user_id, text, parse_mode=ParseMode.HTML)
#             sent += 1
#         except Exception as e:
#             logging.warning(f"Не отправлено пользователю {user.tg_user_id}: {e}")
#             failed += 1
#
#     await state.clear()
#     await message.answer(f"Рассылка завершена!\nУспехов: {sent}, ошибок: {failed}", parse_mode=ParseMode.HTML)
