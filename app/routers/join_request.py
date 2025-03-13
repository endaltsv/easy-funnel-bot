import logging
from aiogram import Router, Bot
from aiogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardMarkup
from aiogram.enums import ParseMode

from app.services.funnel_service import get_funnel
from app.services.user_service import save_user

router = Router()


@router.chat_join_request()
async def handle_chat_join_request(chat_join_request: ChatJoinRequest, bot: Bot):
    channel_id_str = str(chat_join_request.chat.username or chat_join_request.chat.id)
    funnel_data = await get_funnel(channel_id_str)

    user_id = chat_join_request.from_user.id
    username = chat_join_request.from_user.username or ""
    # Сохраняем пользователя

    try:
        await save_user(user_id, username, channel_id_str)
    except Exception as e:
        logging.exception(e)

    if not funnel_data:
        logging.info(f"Нет воронки для канала {channel_id_str}, пропускаем.")
        return

    text_to_send = funnel_data.text or ""
    button_type = funnel_data.button_type
    button_text = funnel_data.button_text
    button_url = funnel_data.button_url

    reply_markup = None
    if button_type == "inline" and button_text and button_url:
        inline_keyboard = [[InlineKeyboardButton(text=button_text, url=button_url)]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    elif button_type == "reply" and button_text and button_url:
        keyboard = [[KeyboardButton(text=button_text, url=button_url)]]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

    try:
        await bot.send_message(chat_id=user_id, text=text_to_send, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        # Если нужно авто-одобрение:
        # await bot.approve_chat_join_request(chat_id=chat_join_request.chat.id, user_id=user_id)
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение {user_id}: {e}")
