from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

shipping_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='SHOP Заказы ожидающие оплаты'),
        ],
        [
            KeyboardButton(text='SHOP Отмененные заказы'),
        ],
        [
            KeyboardButton(text='SHOP Исполненные заказы'),
        ],
    ], resize_keyboard=True
)
