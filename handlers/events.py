from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message

from db import models
from fsm import FSM_state
from keyboards.keyboards import (
    button_group,
    button_unv,
    change_data_keyb,
    timetable_keyb,
    university_keyb,
)
from lexicon.lexicon import LEXICON_RU

router = Router()
storage = MemoryStorage()

@router.message(Command(commands="cancel"))
async def help_command(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON_RU["cancel"], parse_mode= ParseMode.HTML
    )
    await state.set_state(default_state)


@router.message(Command(commands="help"))
async def cancel_command(message: Message):
    await message.answer(
        text=LEXICON_RU["helpik"], parse_mode= ParseMode.HTML
    )

@router.message(Command(commands="profile"))
async def profile_command(message: Message):
    user = await models.User.get(id=message.from_user.id)

    university = user.university or "❌ Не указан"
    group_name = user.group_name or "❌ Не указана"

    await message.answer(
        text=(
            f"{LEXICON_RU['profile'].format(username = message.from_user.first_name)}"
            f"🏫 Вуз: {university}\n"
            f"📚 Группа: {group_name}\n\n"
            f"✏️ Изменить данные — /changedata"
        ),
        parse_mode=ParseMode.HTML
    )


@router.message(Command(commands="changedata"))
async def changedata(message: Message):
    user = await models.User.get(id=message.from_user.id)
    await user.save()
    await message.answer(
        text=LEXICON_RU["change"], reply_markup=change_data_keyb
    )

@router.callback_query(F.data == button_unv.callback_data)
async def changeunv(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text= "Выбери свой университет!🎓\n\nЕсли передумал менять данные скажи Жаворонку 🦜 - /cancel", reply_markup=university_keyb, parse_mode= ParseMode.HTML
    )
    await state.set_state(FSM_state.change_university)
    await callback.answer()

@router.callback_query(StateFilter(FSM_state.change_university))
async def changeunv_callback(callback: CallbackQuery, state: FSMContext):
    user = await models.User.get(id=callback.from_user.id)
    user.university = callback.data
    await user.save()
    await state.set_state(default_state)
    await callback.message.answer(LEXICON_RU["complete"])
    await callback.answer()


@router.callback_query(F.data == button_group.callback_data )
async def changegroup(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text= "📝 Напиши свою группу! 📚\n\nЕсли передумал менять данные скажи Жаворонку 🦜 - /cancel", parse_mode= ParseMode.HTML
    )
    await state.set_state(FSM_state.change_group)
    await callback.answer()

@router.message(StateFilter(FSM_state.change_group))
async def changegroup_message(message : Message, state: FSMContext):
    user = await models.User.get(id=message.from_user.id)
    user.group_name = message.text
    await user.save()
    await state.set_state(default_state)
    await message.answer(LEXICON_RU["complete"])
    await message.answer()

@router.message(Command(commands= "timetable"))
async def choice_timetable(message : Message):
    user = await models.User.get(id=message.from_user.id)
    await message.answer("Скоро сдесь будет расписание!",reply_markup=timetable_keyb)