from aiogram.types import Message
from aiogram import F
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU
from aiogram import Router
from keyboards.keyboards import yes_no, restart_keyb

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],reply_markup = yes_no)

@router.message(F.text == 'В другой раз')
async def restart(message: Message):
    await message.answer(text = LEXICON_RU['restart'], reply_markup= restart_keyb)



@router.message(Command(commands  = 'help') & F.text == 'Мне нужна помощь')
async def process_help_commans(message: Message):
    await message.answer(text=LEXICON_RU['/help'])