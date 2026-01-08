from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from aiogram import Router

router = Router()

@router.message()
async def send_echo(message: Message):
    try:
        await message.reply(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])