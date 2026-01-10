from datetime import date

import pytz
from aiogram.types import (
                           InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

tz = pytz.timezone("Asia/Novosibirsk")

button_yes = KeyboardButton(text=LEXICON_RU["yes_button"])
button_no = KeyboardButton(text=LEXICON_RU["no_button"])

button_asmu = InlineKeyboardButton(text="🏥 АГМУ", callback_data="АГМУ")
button_altgtu = InlineKeyboardButton(text="🛠️ АлтГТУ", callback_data="АлтГТУ")

button_unv  = InlineKeyboardButton(text="🎓Вуз", callback_data="Вуз")
button_group = InlineKeyboardButton(text="📚Группа", callback_data="Группа")

button_timetable_today = InlineKeyboardButton(text = "📅 Сегодня", callback_data= "1")
button_timetable_tommorow = InlineKeyboardButton(text = "📅 Завтра", callback_data= "2")
button_timetable_week = InlineKeyboardButton(text = "🗓️ Неделя", callback_data= "3")
button_timetable_two_week = InlineKeyboardButton(text = "🗓️ Две недели", callback_data= "4")
button_timetable_userdate = InlineKeyboardButton(text = "📅 Своя дата", callback_data= "5")

builder = InlineKeyboardBuilder()
builder.row(button_timetable_today, button_timetable_tommorow)
builder.row(button_timetable_week, button_timetable_two_week)
builder.row(button_timetable_userdate)
timetable_keyb = builder.as_markup()

change_data_keyb = InlineKeyboardMarkup(
    inline_keyboard=[[button_unv, button_group]],
    one_time_keyboard=True,
    resize_keyboard=True,
)

university_keyb = InlineKeyboardMarkup(
    inline_keyboard=[[button_asmu], [button_altgtu]]
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[[button_yes, button_no]],
    one_time_keyboard=True,
    resize_keyboard=True,
)
