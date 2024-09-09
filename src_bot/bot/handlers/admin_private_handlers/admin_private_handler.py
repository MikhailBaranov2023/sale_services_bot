from aiogram import Bot, types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.handlers.admin_private_handlers.admin_game_handlers import games_router
from src_bot.bot.handlers.admin_private_handlers.admin_menu_handlers import admin_main_menu_roter
from src_bot.bot.keyboards.admin_shipping_kb import shipping_kbd
from src_bot.bot.keyboards.main_menu import user_start_kb

from src_bot.bot.keyboards.admin_services_kb import services_kbd
from src_bot.bot.keyboards.admin_games_kb import game_kbd

from src_bot.bot.handlers.admin_private_handlers.shop_handlers import shop_router
from src_bot.bot.handlers.admin_private_handlers.services_handlers import services_router
from src_bot.bot.handlers.admin_private_handlers.admin_banners_handler import banner_router


admin_private_router = Router()
admin_private_router.include_routers(shop_router, services_router, games_router, banner_router,admin_main_menu_roter,)


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


@admin_private_router.message(F.text == 'user')
async def user_menu(message: types.Message, bot: Bot, state: FSMContext):
    if message.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            if message.from_user.id in bot.my_admins_list:
                await message.answer('Меню пользователя', reply_markup=user_start_kb)
    else:
        pass
