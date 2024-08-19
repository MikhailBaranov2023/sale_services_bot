from aiogram import Bot, types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.handlers.admin_private_handlers.game_handlers import games_router
from src_bot.bot.keyboards.admin_shipping_kb import shipping_kbd
from src_bot.bot.keyboards.main_menu import admin_start_kb

from src_bot.database.orm_query.orm_product import orm_create_product
from src_bot.bot.keyboards.admin_services_kb import services_kbd
from src_bot.bot.keyboards.admin_games_kb import game_kbd

from src_bot.bot.handlers.admin_private_handlers.shop_handlers import shop_router
from src_bot.bot.handlers.admin_private_handlers.services_handlers import services_router

admin_private_router = Router()
admin_private_router.include_routers(shop_router, services_router, games_router)


@admin_private_router.message(F.text == 'Доставка')
async def services(message: types.Message, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await message.answer(message.text, reply_markup=shipping_kbd)
    else:
        await message.answer(message.text)


@admin_private_router.message(F.text == 'Cервисы')
async def services(message: types.Message, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await message.answer(message.text, reply_markup=services_kbd)
    else:
        await message.answer(message.text)


@admin_private_router.message(F.text == 'Игры')
async def games(message: types.Message, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await message.answer(message.text, reply_markup=game_kbd)
    else:
        await message.answer(message.text)
