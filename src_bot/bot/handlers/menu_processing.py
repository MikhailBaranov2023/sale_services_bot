from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto
from src_bot.database.orm_query.orm_product import orm_get_product
from src_bot.bot.keyboards.inline import get_user_ps_btns, get_user_catalog_btns, get_user_product_btns, get_game_btns
from src_bot.database.orm_query.orm_product import orm_get_product_ps_subs
from src_bot.database.orm_query.orm_banners import orm_get_banner_ps


async def ps_store_menu(session, level, menu_name):
    print('ps_store_menu')
    banner = await orm_get_banner_ps(session=session, type=menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)
    kbd = get_user_ps_btns(level=level)

    return image, kbd


async def catalog(session, level, menu_name):
    print('catalog')
    banner = await orm_get_banner_ps(session=session, type=menu_name.title())
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    products = await orm_get_product_ps_subs(session=session, name=menu_name)
    kbds = get_user_catalog_btns(level=level, products=products)
    return image, kbds


async def product(session, level, product_id):
    menu_name = None
    print('product')
    current_product = await orm_get_product(session=session, id=product_id)
    if 'essential'.title() in current_product.title:
        menu_name = "essential"
    elif 'extra'.title() in current_product.title:
        menu_name = "extra"
    elif 'deluxe'.title() in current_product.title:
        menu_name = "deluxe"
    image = InputMediaPhoto(media=current_product.image,
                            caption=f"{current_product.title}\n\nЦена - {round(current_product.price, 0)} руб\n\n{current_product.description}")
    kbds = get_user_product_btns(level=level, product=current_product, menu_name=menu_name)
    return image, kbds


async def buy_game(session, level, menu_name):
    print('buy game')
    banner = await orm_get_banner_ps(session=session, type=menu_name.title())
    image = InputMediaPhoto(media=banner.image, caption=banner.description)
    kbds = get_game_btns(level=level)
    return image, kbds


async def get_menu_content(
        session: AsyncSession,
        level: int,
        menu_name: str,
        product_id: int | None = None
):
    if level == 0:
        return await ps_store_menu(session, level, menu_name)
    elif level == 1 and menu_name != 'Game':
        return await catalog(session, level, menu_name)
    elif level == 1 and menu_name == 'Game':
        return await buy_game(session, level, menu_name)
    elif level == 2:
        return await product(session, level, product_id)
