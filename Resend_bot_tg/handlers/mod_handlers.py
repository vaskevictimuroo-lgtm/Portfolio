#mod_handlers.py

from aiogram import Router
from aiogram.types import Message
import database
import config
from aiogram.filters import Command

def check_message(message: Message):
    is_moderator_chat = str(message.chat.id) == str(config.MODERATOR_CHAT_ID)
    is_reply = message.reply_to_message is not None
    return is_moderator_chat and is_reply

def get_link(message: Message):
    moderator_chat_message_id = message.reply_to_message.message_id
    result = database.give_link(moderator_chat_message_id)
    return result

router = Router()

@router.message(Command("chatid"))
async def get_chat_id(message: Message):
    await message.reply(f"🆔 ID этого чата: `{message.chat.id}`")

@router.message(lambda message: str(message.chat.id) == str(config.MODERATOR_CHAT_ID))
async def handle_message(message: Message):
    print("Сообщение принято!")
    text = f"""В базе данных не найдено данное сообщение, скорее всего произошла ошибка базы данных"""
    text1 = f"""Ответ модератора: {message.text}"""
    if check_message(message):
        print("Прошло проверку")
        link = get_link(message)
        if link:
            print("Ссылка найдена")
            user_id, user_message_id = link
            await message.bot.send_message(
                chat_id=user_id,
                text=text1
            )
            await message.bot.send_message(
                chat_id=config.MODERATOR_CHAT_ID,
                text="Сообщение отправлено!"
            )
        else:
            await message.bot.send_message(
                chat_id = message.chat.id,
                text = text
            )
