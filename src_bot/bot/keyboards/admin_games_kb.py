from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

game_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='GAME Заказы ожидающие рассчета'),
        ],
        [
            KeyboardButton(text='GAME Отмененные заказы'),
        ],
        [
            KeyboardButton(text='GAME Оплаченные заказы, ожидающие исполнения'),
        ],
        [
            KeyboardButton(text='GAME Добавить товар'),KeyboardButton(text='GAME Изменить товар')
        ],
        [
            KeyboardButton(text='Добавить баннер PS')
        ],
        [
            KeyboardButton(text='Главное меню')
        ],
    ], resize_keyboard=True
)
