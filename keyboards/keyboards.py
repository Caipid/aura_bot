from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from lexicon.lexicon import LEXICON_RU

button_yes = KeyboardButton(text=LEXICON_RU["yes_button"])
button_no = KeyboardButton(text=LEXICON_RU["no_button"])
button_restart_help = KeyboardButton(text=LEXICON_RU["help_restart_button"])
button_restart_yes = KeyboardButton(text=LEXICON_RU["yes_restart_button"])

button_asmu = InlineKeyboardButton(text="АГМУ", callback_data="АГМУ")
button_altgtu = InlineKeyboardButton(text="АлтГТУ", callback_data="АлтГТУ")

university_keyb = InlineKeyboardMarkup(
    inline_keyboard=[[button_asmu], [button_altgtu]]
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[[button_yes, button_no]],
    one_time_keyboard=True,
    resize_keyboard=True,
)

restart_keyb = ReplyKeyboardMarkup(
    keyboard=[[button_restart_yes, button_restart_help]],
    one_time_keyboard=True,
    resize_keyboard=True,
)
