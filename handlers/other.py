from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU

router = Router()

@router.message()
async def send_echo(message: Message):
    try:
        await message.reply(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Жаворонок еще не видал такого! Для списка команд - /help', parse_mode= ParseMode.HTML)