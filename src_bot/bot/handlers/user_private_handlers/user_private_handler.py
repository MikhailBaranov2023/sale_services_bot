from aiogram.filters import CommandStart, StateFilter, or_f, Command
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.handlers.user_private_handlers.user_profile_handler import user_profile_router
from src_bot.bot.handlers.user_private_handlers.user_services_order_handler import user_services_order_router
from src_bot.bot.keyboards.main_menu import user_start_kb, admin_short_kb
from src_bot.bot.keyboards.games_keyboards import games_kbd
from src_bot.bot.keyboards.shop_keyboard import inline_kbd, inline_services_kbd
from src_bot.bot.keyboards.profile_kbd import profile_kbd, register_kbd
from src_bot.database.orm_query.orm_users import orm_check_user_chat_id

from src_bot.database.orm_query.orm_product import orm_get_product_shop, orm_get_product_services
from src_bot.bot.handlers.user_private_handlers.user_game_handler import user_game_router
from src_bot.bot.handlers.user_private_handlers.user_order_shop_handler import user_shop_order

user_private_router = Router()
user_private_router.include_routers(user_game_router, user_shop_order, user_services_order_router,
                                    user_profile_router, )


@user_private_router.message(CommandStart())
async def start(message: types.Message, bot: Bot, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        if message.from_user.id in bot.my_admins_list:
            await message.answer('Вы в админке', reply_markup=admin_short_kb)
        else:
            if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
                await message.answer(
                    'Этот бот поможет вам быстро и с минимальной комиссией оплатить любые зарубежные сервисы.\n\n Для того чтобы продолжить вам необходимо зарегистрироваться. ',
                    reply_markup=register_kbd)
            else:
                await message.answer('Рады видеть вас снова', reply_markup=user_start_kb)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_private_router.message(or_f(F.text == "Профиль", Command('profile')))
async def profile_keyboard(message: types.Message, session: AsyncSession, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
            await message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                 reply_markup=register_kbd)
        else:
            await message.answer(text=message.text, reply_markup=profile_kbd)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_private_router.message(or_f(F.text == "Главное меню", Command('menu')))
async def games_keyboard(message: types.Message, bot: Bot, session: AsyncSession):
    if message.from_user.id in bot.my_admins_list:
        await message.answer('Вы в админке', reply_markup=admin_short_kb)
    else:
        if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
            await message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                 reply_markup=register_kbd)
        else:
            await message.answer(message.text, reply_markup=user_start_kb)


@user_private_router.message(or_f(F.text == "Доставка товаров", Command('shop')))
async def shop_add_product(message: types.Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
            await message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                 reply_markup=register_kbd)
        else:
            product = await orm_get_product_shop(session=session)
            await message.answer_photo(photo=product.image, caption=f"{product.title}\n\n{product.description}",
                                       reply_markup=inline_kbd)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_private_router.message(or_f(F.text == 'Оплата сервисов', Command('services')))
async def pay_services(message: types.Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
            await message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                 reply_markup=register_kbd)
        else:
            product = await orm_get_product_services(session=session)

            await message.answer_photo(photo=product.image,
                                       caption=f"{product.title}\n\nКомиссия 5%. Минимальная от {round(product.price, 2)}руб.\n\n{product.description}",
                                       reply_markup=inline_services_kbd)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_private_router.message(or_f(F.text == "Игровые платформы", Command('games')))
async def games_keyboard(message: types.Message, session: AsyncSession, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
            await message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                 reply_markup=register_kbd)
        else:
            await message.answer(text=message.text, reply_markup=games_kbd)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


"""cancel handlers """


@user_private_router.callback_query(StateFilter('*'), F.data == 'cancel')
async def cancel_handler_data(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state is None:
        if callback_query.from_user.id in bot.my_admins_list:
            await callback_query.message.answer(text='Отменить', reply_markup=admin_short_kb)
        else:
            await callback_query.message.answer(text='Отменить', reply_markup=user_start_kb)
    else:
        await state.clear()
        if callback_query.from_user.id in bot.my_admins_list:
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
            await callback_query.message.answer('Панель администратора', reply_markup=admin_short_kb)
        else:
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
            await callback_query.message.answer('Главное меню', reply_markup=user_start_kb)


@user_private_router.message(StateFilter('*'), Command('cancel'))
@user_private_router.message(StateFilter('*'), F.text.lower().casefold() == 'назад')
@user_private_router.message(StateFilter('*'), or_f(F.text.lower().casefold() == 'отменить'))
async def cancel_handler(message: types.Message, state: FSMContext, bot: Bot) -> None:
    current_state = await state.get_state()
    if current_state is None:
        if message.from_user.id in bot.my_admins_list:
            await message.answer(message.text, reply_markup=admin_short_kb)
        else:
            await message.answer(message.text, reply_markup=user_start_kb)
    else:
        await state.clear()
        if message.from_user.id in bot.my_admins_list:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await message.answer('Действия отменены', reply_markup=admin_short_kb)
        else:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await message.answer('Действия отменены', reply_markup=user_start_kb)
