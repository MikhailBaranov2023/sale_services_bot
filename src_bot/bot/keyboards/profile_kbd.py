from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

profile_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мои заказы'),
            KeyboardButton(text='Подписаться на уведомления'),
        ],
        # [
        #     KeyboardButton(text='Получить реферальный код'),
        # ],
        [
            KeyboardButton(text='Главное меню')
        ]

    ],
    resize_keyboard=True,
)

register_kbd = ReplyKeyboardMarkup(
    keyboard=[

        [KeyboardButton(text='Зарегистрироваться', request_contact=True)], [KeyboardButton(text='Назад')]

    ],
    resize_keyboard=True,
)

my_orders_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мои заказы в доставке'),
            KeyboardButton(text='Заказы по оплате сервисов'),
        ],
        [
          KeyboardButton(text='Профиль')
        ],
    ], resize_keyboard=True
)
