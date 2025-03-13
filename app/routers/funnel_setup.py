import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.enums import ParseMode

from app.config.settings import ADMIN_ID
from app.services.funnel_service import upsert_funnel

router = Router()


class FunnelStates(StatesGroup):
    waiting_for_channel_id = State()
    waiting_for_message_text = State()
    waiting_for_add_button = State()
    waiting_for_button_type = State()
    waiting_for_button_text = State()
    waiting_for_button_url = State()


@router.message(Command(commands="create_funnel"))
async def cmd_start(message: Message, state: FSMContext):
    if message.from_user.id != int(ADMIN_ID):
        return

    await state.set_state(FunnelStates.waiting_for_channel_id)
    await message.answer(
        "Привет! Давай создадим воронку.\n"
        "Пришли мне ID или @username канала...",
        parse_mode=ParseMode.HTML
    )


@router.message(FunnelStates.waiting_for_channel_id)
async def get_channel_id(message: Message, state: FSMContext):
    channel_id = message.text.strip()
    await state.update_data(channel_id=channel_id)
    await state.set_state(FunnelStates.waiting_for_message_text)
    await message.answer("Теперь пришли текст сообщения:", parse_mode=ParseMode.HTML)


@router.message(FunnelStates.waiting_for_message_text)
async def get_message_text(message: Message, state: FSMContext):
    text = message.html_text
    await state.update_data(text=text)

    await state.set_state(FunnelStates.waiting_for_add_button)
    await message.answer("Добавим кнопку? да/нет", parse_mode=ParseMode.HTML)


@router.message(FunnelStates.waiting_for_add_button)
async def ask_add_button(message: Message, state: FSMContext):
    choice = message.text.lower()
    data = await state.get_data()

    if choice in ["да", "yes", "y", "д"]:
        await state.set_state(FunnelStates.waiting_for_button_type)
        await message.answer("Тип кнопки? inline/reply", parse_mode=ParseMode.HTML)
    else:
        # Сохраняем без кнопки
        await upsert_funnel(
            channel_id=data["channel_id"],
            text=data["text"],
            button_type=None,
            button_text=None,
            button_url=None
        )
        await state.clear()
        await message.answer("Воронка сохранена без кнопки!", parse_mode=ParseMode.HTML)


@router.message(FunnelStates.waiting_for_button_type)
async def ask_button_type(message: Message, state: FSMContext):
    button_type = message.text.lower()
    if button_type not in ["inline", "reply"]:
        await message.answer("Нужно inline или reply. Попробуй ещё раз.")
        return

    await state.update_data(button_type=button_type)
    await state.set_state(FunnelStates.waiting_for_button_text)
    await message.answer("Текст кнопки?", parse_mode=ParseMode.HTML)


@router.message(FunnelStates.waiting_for_button_text)
async def ask_button_text(message: Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await state.set_state(FunnelStates.waiting_for_button_url)
    await message.answer("URL кнопки?", parse_mode=ParseMode.HTML)


@router.message(FunnelStates.waiting_for_button_url)
async def finish_funnel_setup(message: Message, state: FSMContext):
    await state.update_data(button_url=message.text)

    data = await state.get_data()

    await upsert_funnel(
        channel_id=data["channel_id"],
        text=data["text"],
        button_type=data["button_type"],
        button_text=data["button_text"],
        button_url=data["button_url"]
    )

    await state.clear()
    await message.answer("Воронка успешно сохранена!", parse_mode=ParseMode.HTML)
