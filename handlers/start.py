from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message

from db import models
from fsm import FSM_state
from keyboards.keyboards import university_keyb, yes_no
from lexicon.lexicon import LEXICON_RU

router = Router()
storage = MemoryStorage()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    exists = await models.User.exists(id=message.from_user.id)
    if exists:
        await message.answer(text=LEXICON_RU["exists"].format(username = message.from_user.first_name), parse_mode = ParseMode.HTML)
    else:
        await message.answer(text=LEXICON_RU["start"].format(username = message.from_user.first_name), reply_markup=yes_no)


@router.message(
    F.text == LEXICON_RU["yes_button"], StateFilter(default_state)
)
async def ask_university(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU["know_university"], reply_markup=university_keyb
    )
    await state.set_state(FSM_state.fill_university)


@router.callback_query(StateFilter(FSM_state.fill_university))
async def process_university_callback(
    callback: CallbackQuery, state: FSMContext
):
    await state.update_data(university=callback.data)
    await state.set_state(FSM_state.fill_group)
    await callback.message.answer(LEXICON_RU["know_group"])
    await callback.answer()


@router.message(StateFilter(FSM_state.fill_group))
async def process_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    data = await state.get_data()
    await models.User.update_or_create(
        id=message.from_user.id,
        university=data["university"],
        group_name=data["group"],
    )
    await message.answer(
        f"Готово ✅\nВУЗ: {data['university']}\nГруппа: {data['group']}"
    )
    await state.clear()
