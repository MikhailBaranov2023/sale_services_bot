from aiogram import Bot, types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.handlers.admin_private_handlers.admin_game_handlers import games_router
from src_bot.bot.handlers.admin_private_handlers.admin_menu_handlers import admin_main_menu_roter

from src_bot.bot.keyboards.main_menu import user_start_kb

from src_bot.bot.handlers.admin_private_handlers.shop_handlers import shop_router
from src_bot.bot.handlers.admin_private_handlers.services_handlers import services_router
from src_bot.bot.handlers.admin_private_handlers.admin_banners_handler import banner_router
from src_bot.database.orm_query.orm_banners import orm_get_banner_ps, orm_update_photo_banner, orm_update_photo_PS_Store
from src_bot.database.orm_query.orm_product import orm_update_description_to_shop, orm_update_image_to_shop, \
    orm_update_image_to_services, orm_update_image_to_ps, get_product_to_title

admin_private_router = Router()
admin_private_router.include_routers(shop_router, services_router, games_router, banner_router, admin_main_menu_roter, )


class Product(StatesGroup):
    image = State()


@admin_private_router.message(F.text == 'Изменить фото для ps')
async def admin_private_handler(message: types.Message, state: FSMContext, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await state.set_state(Product.image)
        await message.answer('Добавьте фото')


@admin_private_router.message(Product.image, F.photo)
async def update_description(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    image = data['image']
    await orm_update_image_to_ps(session=session, image=image)
    await state.clear()
    await message.answer('Изменено')


class Banners(StatesGroup):
    image = State()


@admin_private_router.message(F.text == 'Изменить фото для баннера')
async def admin_private_handler(message: types.Message, state: FSMContext, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await state.set_state(Banners.image)
        await message.answer('Добавьте фото')


@admin_private_router.message(Banners.image, F.photo)
async def update_description(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    image = data['image']
    print(image)
    try:
        await orm_update_photo_PS_Store(session=session, image=image)
        await state.clear()
        await message.answer('Изменено')
    except Exception as e:
        print(e)
