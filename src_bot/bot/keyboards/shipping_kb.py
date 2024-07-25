from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

shipping_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Текущие заказы в доставке'),
        ],
        [
            KeyboardButton(text='Отмененные заказы в доставке'),
        ],
        [
            KeyboardButton(text='Исполненные заказы в доставке'),
        ],
    ], resize_keyboard=True
)
