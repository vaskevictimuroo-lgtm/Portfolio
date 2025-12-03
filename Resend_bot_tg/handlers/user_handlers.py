#user_handlers.py

from aiogram import Router
from aiogram.types import Message
import database
import config

router = Router()

def take_info(sent_msg, message):
    moderator_chat_message_id = sent_msg.message_id
    user_id = message.from_user.id
    user_message_id = message.message_id
    database.save_link(moderator_chat_message_id, user_id, user_message_id)

@router.message(lambda message: message.chat.type == "private")
async def handle_all_messages(message: Message):
    if str(message.chat.id) == str(config.MODERATOR_CHAT_ID):
        return
    if message.from_user.is_bot:
        return
    user_info_text = f"""Сообщение от {message.from_user.full_name} (@{message.from_user.username}), ID: {message.from_user.id}: {message.text}"""
    user_info_media = f"""Сообщение от {message.from_user.full_name} (@{message.from_user.username}), ID: {message.from_user.id}:
Медиа приложены ниже"""
    print(f"Сообщение принято: {message.from_user.id}")
    await message.answer("Сообщение принято!")
    if message.text:
        sent_msg = await message.bot.send_message(
            chat_id=config.MODERATOR_CHAT_ID,
            text=user_info_text)
        take_info(sent_msg, message)
    if not message.text:
        await message.bot.send_message(
            chat_id=config.MODERATOR_CHAT_ID,
            text=user_info_media
        )
        sent_msg = await message.bot.forward_message(
            chat_id=config.MODERATOR_CHAT_ID,
            from_chat_id = message.chat.id,
            message_id = message.message_id
        )
        take_info(sent_msg, message)

