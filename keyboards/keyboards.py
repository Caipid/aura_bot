from aiogram.types import (
                           InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardMarkup,
)

from lexicon.lexicon import LEXICON_RU

button_yes = KeyboardButton(text=LEXICON_RU["yes_button"])
button_no = KeyboardButton(text=LEXICON_RU["no_button"])

button_asmu = InlineKeyboardButton(text="🏥 АГМУ", callback_data="АГМУ")
button_altgtu = InlineKeyboardButton(text="🛠️ АлтГТУ", callback_data="АлтГТУ")

button_unv  = InlineKeyboardButton(text="🎓Вуз", callback_data="Вуз")
button_group = InlineKeyboardButton(text="📚Группа", callback_data="Группа")

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
