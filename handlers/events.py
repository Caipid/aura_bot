from datetime import date, timedelta, timezone

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message

import parser
from db import models
from fsm import FSM_state
from keyboards.keyboards import (
    button_group,
    button_timetable_today,
    button_timetable_tommorow,
    button_timetable_two_week,
    button_timetable_userdate,
    button_timetable_week,
    button_unv,
    change_data_keyb,
    timetable_keyb,
    university_keyb,
)
from lexicon.dayweek import days
from lexicon.lexicon import LEXICON_RU

tz = timezone(timedelta(hours = 7), name = "Novosibirsk")
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
    await message.answer("Выбери дату и Жаворонок🦜 подскажет расписание⏰📅🕊️! \n\n\nПередумал смотреть😥💔,\nСкажи Жаворонку 🦜 - /cancel", parse_mode= ParseMode.HTML,reply_markup=timetable_keyb)







@router.callback_query(F.data == button_timetable_today.callback_data)
async def timetable_today(callback: CallbackQuery):
    user = await models.User.get(id=callback.from_user.id) #активная сессия
    data_timetable = date.today().strftime("%d.%m.%Y") # разворот даты
    today = date.today().isoweekday()
    await callback.message.answer(LEXICON_RU["timetable_ready"].format(date = data_timetable, weekday = days[str(today)] ), parse_mode= ParseMode.HTML)
    await callback.answer()













@router.callback_query(F.data == button_timetable_tommorow.callback_data)
async def timetable_tommorow(callback: CallbackQuery):
    data_timetable = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    today = (date.today() + timedelta(days=1)).isoweekday()
    user = await models.User.get(id=callback.from_user.id)
    await callback.message.answer(LEXICON_RU["timetable_ready"].format(date = data_timetable, weekday = days[str(today)] ), parse_mode= ParseMode.HTML)
    await callback.answer()





@router.callback_query(F.data == button_timetable_week.callback_data)
async def timetable_week(callback: CallbackQuery, ):
    user = await models.User.get(id=callback.from_user.id)
    data_timetable_start = date.today().strftime("%d.%m.%Y")
    data_timetable_end = (date.today() + timedelta(days=7)).strftime("%d.%m.%Y")
    day_start = date.today().isoweekday()
    day_end = (date.today() + timedelta(days=7)).isoweekday()
    await callback.message.answer(LEXICON_RU["timetable_week"].format(date = data_timetable_start, weekday = days[str(day_start)],
                                                                       date2 = data_timetable_end, weekday2 = days[str(day_end)] ), parse_mode= ParseMode.HTML)

    timetable = await parser.get_data(2,data_timetable_start,user.group_name)
    for lesson in timetable:
        text = LEXICON_RU["timetable_week"].format(date = data_timetable_start, weekday = days[str(day_start)],
                                                                       date2 = data_timetable_end, weekday2 = days[str(day_end)] )
        + LEXICON_RU["\n\nПервая Пара:"].format(discipline=lesson["discipline"])
        + LEXICON_RU["timetable"].format(discipline=lesson["discipline"])
        + LEXICON_RU["timetable"].format(discipline=lesson["discipline"])
        + LEXICON_RU["timetable"].format(discipline=lesson["discipline"])
        + LEXICON_RU["timetable"].format(discipline=lesson["discipline"])
        await callback.message.answer(text, parse_mode=ParseMode.HTML)
    await callback.answer()



@router.callback_query(F.data == button_timetable_two_week.callback_data)
async def timetable_two_week(callback: CallbackQuery):
    data_timetable_start = date.today().strftime("%d.%m.%Y")
    data_timetable_end = (date.today() + timedelta(days=14)).strftime("%d.%m.%Y")
    day_start = date.today().isoweekday()
    day_end = (date.today() + timedelta(days=14)).isoweekday()
    await callback.message.answer(LEXICON_RU["timetable_week"].format(date = data_timetable_start, weekday = days[str(day_start)],
                                                                       date2 = data_timetable_end, weekday2 = days[str(day_end)] ), parse_mode= ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == button_timetable_userdate.callback_data)
async def timetable_userdate(callback: CallbackQuery):
    data_timetable = date.today().strftime("%d.%m.%Y")
    today = date.today().isoweekday()
    user = await models.User.get(id=callback.from_user.id)
    await callback.message.answer(LEXICON_RU["timetable_ready"].format(date = data_timetable, weekday = days[str(today)] ), parse_mode= ParseMode.HTML)
    await callback.answer()