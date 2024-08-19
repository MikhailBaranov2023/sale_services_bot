from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

shipping_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='SHOP Заказы ожидающие рассчета'),
        ],
        [
            KeyboardButton(text='SHOP Отмененные заказы'),
        ],
        [
            KeyboardButton(text='SHOP Оплаченные заказы, ожидающие доставки'),
        ],
        [
          KeyboardButton(text='SHOP Заказы в доставке')
        ],
        [
            KeyboardButton(text='SHOP Добавить товар')
        ],
        [
          KeyboardButton(text='Главное меню')
        ],
    ], resize_keyboard=True
)
