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
        text= "Выбери свой университет!🎓\n\nЕсли передумал менять данные скажи Жаворонку 🦉 - /cancel", reply_markup=university_keyb, parse_mode= ParseMode.HTML
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
        text= "📝 Напиши свою группу! 📚\n\nЕсли передумал менять данные скажи Жаворонку 🦉 - /cancel", parse_mode= ParseMode.HTML
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
    await message.answer("Выбери дату и Жаворонок🦉 подскажет расписание⏰📅🕊️! \n\n\nПередумал смотреть😥💔,\nСкажи Жаворонку 🦉 - /cancel", parse_mode= ParseMode.HTML,reply_markup=timetable_keyb)





@router.callback_query(F.data == button_timetable_today.callback_data)
async def timetable_today(callback: CallbackQuery):
    user = await models.User.get(id=callback.from_user.id)
    data_timetable = date.today().strftime("%d.%m.%Y") # разворот даты
    today = date.today().isoweekday()
    timetable = await parser.get_data(1,data_timetable,user.group_name)
    await callback.message.answer(LEXICON_RU["timetable_ready"].format(date = data_timetable, weekday = days[str(today)] ), parse_mode= ParseMode.HTML)
    texts = processing_tt(timetable)
    for text in texts:
        await callback.message.answer(text, parse_mode=ParseMode.HTML)
    await callback.message.answer(LEXICON_RU["timetable_end"], parse_mode=ParseMode.HTML)
    await callback.answer()


@router.callback_query(F.data == button_timetable_tommorow.callback_data)
async def timetable_tommorow(callback: CallbackQuery):
    data_timetable = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    today = (date.today() + timedelta(days=1)).isoweekday()
    user = await models.User.get(id=callback.from_user.id)
    await callback.message.answer(LEXICON_RU["timetable_ready"].format(date = data_timetable, weekday = days[str(today)] ), parse_mode= ParseMode.HTML)
    timetable = await parser.get_data(1,data_timetable,user.group_name)
    texts = processing_tt(timetable)
    for text in texts:
        await callback.message.answer(text, parse_mode=ParseMode.HTML)
    await callback.message.answer(LEXICON_RU["timetable_end"], parse_mode=ParseMode.HTML)
    await callback.answer()





@router.callback_query(F.data == button_timetable_week.callback_data)
async def timetable_week(callback: CallbackQuery, ):
    user = await models.User.get(id=callback.from_user.id)

    data_start = (date.today() - timedelta(days=date.today().isoweekday()) + timedelta(1))
    data_end = (data_start + timedelta(days=6))

    day_start = data_start.isoweekday()
    day_end = data_end.isoweekday()

    data_timetable_start = data_start.strftime("%d.%m.%Y")
    data_timetable_end = data_end.strftime("%d.%m.%Y")
    await callback.message.answer(LEXICON_RU["timetable_week"].format(date = data_timetable_start, weekday = days[str(day_start)],
                                                                       date2 = data_timetable_end, weekday2 = days[str(day_end)] ), parse_mode= ParseMode.HTML)
    timetable = await parser.get_data(2,data_timetable_start,user.group_name)
    texts = processing_tt(timetable)
    for text in texts:
        await callback.message.answer(text, parse_mode=ParseMode.HTML)
    await callback.message.answer(LEXICON_RU["timetable_end"], parse_mode=ParseMode.HTML)
    await callback.answer()



@router.callback_query(F.data == button_timetable_two_week.callback_data)
async def timetable_two_week(callback: CallbackQuery):
    user = await models.User.get(id=callback.from_user.id)

    data_start = (date.today() - timedelta(days=date.today().isoweekday()) + timedelta(1))
    data_end = (data_start + timedelta(days=13))

    day_start = data_start.isoweekday()
    day_end = data_end.isoweekday()

    data_timetable_start = data_start.strftime("%d.%m.%Y")
    data_timetable_end = data_end.strftime("%d.%m.%Y")

    await callback.message.answer(LEXICON_RU["timetable_week"].format(date = data_timetable_start, weekday = days[str(day_start)],
                                                                       date2 = data_timetable_end, weekday2 = days[str(day_end)] ), parse_mode= ParseMode.HTML)
    timetable = await parser.get_data_for_month(3,data_start.month,user.group_name)
    texts = processing_tt(timetable,14,data_start)
    for text in texts:
        await callback.message.answer(text, parse_mode=ParseMode.HTML)
    await callback.message.answer(LEXICON_RU["timetable_end"], parse_mode=ParseMode.HTML)
    await callback.answer()



@router.callback_query(F.data == button_timetable_userdate.callback_data)
async def timetable_userdate(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
    "🦉 Привет! Жаворонок ждёт твою дату 😊\n"
    "📅 Напиши в формате: день.месяц.год"
    "\n\n\nПередумал смотреть😥💔,\nСкажи Жаворонку 🦉 - /cancel"
    )
    await state.set_state(FSM_state.custom_data)


@router.message(StateFilter(FSM_state.custom_data))
async def timetable_customdata(message: Message, state: FSMContext):
    data_timetable = message.text
    today = date.today().isoweekday()
    user = await models.User.get(id=message.from_user.id)
    await message.answer(LEXICON_RU["timetable_ready"].format(date = data_timetable, weekday = days[str(today)] ), parse_mode= ParseMode.HTML)
    timetable = await parser.get_data(1,data_timetable,user.group_name)
    texts = processing_tt(timetable)
    for text in texts:
        await message.answer(text, parse_mode=ParseMode.HTML)
    await message.answer(LEXICON_RU["timetable_end"], parse_mode=ParseMode.HTML)
    await state.set_state(default_state)


def processing_tt(timetable,day_check = 0 ,data_st = 0):
    texts_timetable = []

    if timetable:
        current_day = timetable[0]["week_day"]
    else:
        current_day = None
        no_lession_text = "🦉 Кажется, сегодня занятий нет! \n         🎉✨Расслабься и отдохни 😌📚"
        texts_timetable.append(no_lession_text)
        return texts_timetable

    current_text = days[timetable[0]["week_day"]].upper() +"\n"
    current_text +="   [" + timetable[0]["date"] + "]"
    schedule_days = []
    if (day_check == 14):
        for i in range(13):
            schedule_days.append((data_st + timedelta(days=i)).strftime("%d.%m.%Y"))
    else:
        schedule_days = []
    for i in range(len(timetable)):
        if (timetable[i]["date"] in schedule_days or day_check != 14):
            if (timetable[i]["week_day"] == current_day):
                current_text += (
                    f'🕒 {timetable[i]["time_start"]}—{timetable[i]["time_end"]}\n'
                    f'📍 Адрес: {timetable[i]["address"]}\n'
                    f'🚪 Кабинет: {timetable[i]["room"]}\n'
                    f'📘 Предмет: {timetable[i]["discipline"]}\n'
                    '➖➖➖➖➖➖➖➖➖➖\n'
                )
                current_day = timetable[i]["week_day"]
            else:
                texts_timetable.append(current_text)
                current_day = timetable[i]["week_day"]
                current_text = days[current_day].upper() +"\n"
                current_text +="   [" + timetable[i]["date"] + "]"
                current_text += (
                    f'🕒 {timetable[i]["time_start"]}—{timetable[i]["time_end"]}\n'
                    f'📍 Адрес: {timetable[i]["address"]}\n'
                    f'🚪 Кабинет: {timetable[i]["room"]}\n'
                    f'📘 Предмет: {timetable[i]["discipline"]}\n'
                    '➖➖➖➖➖➖➖➖➖➖\n'
                )
    texts_timetable.append(current_text)
    return texts_timetable