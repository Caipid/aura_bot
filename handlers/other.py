from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message

router = Router()

@router.message()
async def send_echo(message: Message):
    try:
        await message.reply(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="🦉 Упс! Жаворонок ещё не видел такого 😅\n" + "📜 Список всех команд — /help", parse_mode= ParseMode.HTML)