from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

games_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='PS Store'),
            KeyboardButton(text='Microsoft Store'),
            KeyboardButton(text='Steam')
        ],
        [
            KeyboardButton(text='Главное меню'),
        ]
    ],
    resize_keyboard=True,
)
