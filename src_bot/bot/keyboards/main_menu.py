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
            KeyboardButton(text='Профиль')
        ]
    ],
    resize_keyboard=True,
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='отменить'),

        ],
    ], resize_keyboard=True
)

admin_short_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заказы ожидающие расчета'),
            KeyboardButton(text='Заказы ожидающие оплаты'),
            KeyboardButton(text='Заказы ожидающие исполнения'),
        ],
        [
            KeyboardButton(text='Заказы в доставке'),
        ],
        [
            KeyboardButton(text='Отмененные заказы'),
        ],
    ], resize_keyboard=True
)
