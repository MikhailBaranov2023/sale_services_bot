from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оплата сервисов'),
            KeyboardButton(text='Игровые платформы'),
            KeyboardButton(text='Доставка товаров')
        ],
        [
            KeyboardButton(text='О нас'),
            KeyboardButton(text='Подписаться')
        ]
    ],
    resize_keyboard=True,
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='отмена'),

        ],
        ], resize_keyboard=True
)
