from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

services_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='SERVICES Заказы ожидающие рассчета'),
        ],
        [
            KeyboardButton(text='SERVICES Отмененные заказы'),
        ],
        [
            KeyboardButton(text='SERVICES Оплаченные заказы, ожидающие исполнения'),
        ],
        [
            KeyboardButton(text='SERVICES Добавить товар')
        ],
        [
            KeyboardButton(text='Главное меню')
        ],
    ], resize_keyboard=True
)
