from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from src_bot.database.orm_query.orm_users import orm_check_user
from sqlalchemy.ext.asyncio import AsyncSession


class MenuCallBack(CallbackData, prefix='menu'):
    level: int
    menu_name: str
    product: int | None = None


def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_inlineMix_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()


def get_user_ps_btns(*, level: int, sizes: tuple[int] = (2, 1, 2, 1)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        'PS+ ESSENTIAL': 'essential',
        'PS+ EXTRA': 'extra',
        'PS+ DELUXE': 'deluxe',
        'Купить игру': 'ps_game',
        'Отзывы': 'feedback',
        'Чем отличаются подписки?': 'Subscription difference',
    }
    for text, menu_name in btns.items():
        if menu_name == 'essential' or menu_name == 'extra' or menu_name == 'deluxe':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1, menu_name=menu_name).pack()))
        elif menu_name == 'buy_ps_game':
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=3, menu_name=menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level, menu_name=menu_name).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_user_catalog_btns(*, level: int, products: list, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    for p in products:
        keyboard.add(InlineKeyboardButton(text=f'{p.title} - {round(p.price, 0)} руб',
                                          callback_data=MenuCallBack(level=level + 1, menu_name=p.title,

                                                                     product=p.id).pack()))
    keyboard.add(
        InlineKeyboardButton(text='Назад', callback_data=MenuCallBack(level=level - 1, menu_name='PS Store').pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_user_product_btns(*, level: int, product, sizes: tuple[int] = (1,), menu_name):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Купить', callback_data=f'psbuy_{product.id}'))
    keyboard.add(
        InlineKeyboardButton(text='Назад', callback_data=MenuCallBack(level=level - 1, menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()
