from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


inline_kbd = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='STOCKX', url='https://stockx.com'),
        InlineKeyboardButton(text='FARFETCH', url='https://www.farfetch.com/')
    ],
    [
        InlineKeyboardButton(text='ASOS', url='https://www.asos.com'),
        InlineKeyboardButton(text='FOOTLOCKER', url='https://www.footlocker.pt')
    ],
    [
        InlineKeyboardButton(text='COURIR', url='https://www.courir.com'),
        InlineKeyboardButton(text='ADIDAS', url='https://www.adidas.com')
    ],
    [
        InlineKeyboardButton(text='NIKE', url='https://www.nike.com'),
        InlineKeyboardButton(text='EBAY', url='https://www.ebay.com')
    ],
    [
        InlineKeyboardButton(text='Заказать', callback_data='make_order',)
    ]
], resize_keyboard=True,

)

inline_services_kbd = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Оставить заявку', callback_data='services')
    ],

], resize_keyboard=True
)