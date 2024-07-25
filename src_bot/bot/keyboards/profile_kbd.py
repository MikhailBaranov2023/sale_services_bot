from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

profile_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мои заказы'),
            KeyboardButton(text='Подписаться на уведомления'),
        ],
        [
            KeyboardButton(text='Получить реферальный код'),
        ],
        [
            KeyboardButton(text='Главное меню')
        ]

    ],
    resize_keyboard=True,
)

register_kbd = ReplyKeyboardMarkup(
    keyboard=[

        [KeyboardButton(text='Зарегистрироваться')],

    ],
    resize_keyboard=True,
)
