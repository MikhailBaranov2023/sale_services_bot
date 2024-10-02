from aiogram.filters import CommandStart, StateFilter, or_f, Command
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.handlers.user_private_handlers.user_profile_handler import user_profile_router
from src_bot.bot.handlers.user_private_handlers.user_services_order_handler import user_services_order_router
from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.main_menu import user_start_kb, admin_short_kb
from src_bot.bot.keyboards.games_keyboards import games_kbd
from src_bot.bot.keyboards.shop_keyboard import inline_kbd, inline_services_kbd
from src_bot.bot.keyboards.profile_kbd import profile_kbd, register_kbd
from src_bot.database.orm_query.orm_order import orm_check_order
from src_bot.database.orm_query.orm_order_shop import orm_check_order_shop
from src_bot.database.orm_query.orm_users import orm_check_user_chat_id, orm_check_user

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
                    'Для того, чтобы продолжить, вам необходимо зарегистрироваться.',
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
            await message.answer('Для того, чтобы продолжить, вам необходимо зарегистрироваться.',
                                 reply_markup=register_kbd)
        else:
            await message.answer(text=message.text, reply_markup=profile_kbd)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_private_router.message(or_f(F.text == "Главное меню", Command('menu')))
async def games_keyboard(message: types.Message, bot: Bot, session: AsyncSession, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        if message.from_user.id in bot.my_admins_list:
            await message.answer('Вы в админке', reply_markup=admin_short_kb)
        else:
            if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
                await message.answer('Для того, чтобы продолжить, вам необходимо зарегистрироваться.',
                                     reply_markup=register_kbd)
            else:
                await message.answer(message.text, reply_markup=user_start_kb)
    else:
        await state.clear()
        if message.from_user.id in bot.my_admins_list:
            await message.answer('Вы в админке', reply_markup=admin_short_kb)
        else:
            if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
                await message.answer('Для того, чтобы продолжить, вам необходимо зарегистрироваться.',
                                     reply_markup=register_kbd)
            else:
                await message.answer(message.text, reply_markup=user_start_kb)


@user_private_router.message(or_f(F.text == "Доставка товаров", Command('shop')))
async def shop_add_product(message: types.Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
            await message.answer('Для того, чтобы продолжить, вам необходимо зарегистрироваться.',
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
            await message.answer('Для того, чтобы продолжить, вам необходимо зарегистрироваться.',
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
            await message.answer('Для того, чтобы продолжить, вам необходимо зарегистрироваться.',
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
            await message.answer('Действия отменены', reply_markup=admin_short_kb)
        else:
            await message.answer('Действия отменены', reply_markup=user_start_kb)


class Message(StatesGroup):
    message = State()


@user_private_router.callback_query(F.data == 'admin_message', StateFilter(None))
async def add_message_to_admin(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.from_user.id in bot.my_admins_list:
        await callback.answer('Вы админ')
    else:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(Message.message)
            await callback.message.answer('Введите ваше сообщение')
        else:
            await state.clear()


@user_private_router.message(Message.message, F.text)
async def send_message_to_admin(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(message=message.text)
    data = await state.get_data()
    text = data['message']
    try:
        await bot.send_message(chat_id=bot.my_admins_list[-1],
                               text=f'Вам новое сообщение от пользователя @{message.from_user.username}\n\nСообщение:\n{text}')
        await state.clear()
        await message.answer('Cообщение отправлено. Скоро с вами свяжется администратор.')
    except Exception as e:
        await state.clear()
        await message.answer('Что то пошло не так. Пожалуйста попробуйте позже.')


@user_private_router.callback_query(F.data.startswith('ipaid_'))
async def paid_order(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    try:
        order = await orm_check_order(session, order_id=int(callback.data.split('_')[-1]))
        user = await orm_check_user(session=session, user_id=order.user_id)
        await bot.send_message(chat_id=bot.my_admins_list[-1],
                               text=f"#{order.type}\n\nПользователь оплатил заказ. Проверьте и измените статуc заказа.\n\nДетали заказа:\nCервис для оплаты -{order.url},\nОписание - {order.description},\n\nЗаказ не оплачен.\nСумма к оплате - {round(order.amount, 0)} руб.\nПользователь - {user.user_name}",
                               reply_markup=get_callback_btns(btns={
                                   'Оплачено': f'paid_{order.id}',
                                   'Отменить': f'cancel_{order.id}',
                                   'Написать клиенту': f'message_{order.id}'}))
        await callback.message.answer('В ближайщее время мы проверим оплату. И оплатим ваш сервис.')
    except Exception as e:
        await callback.message.answer('Что то пошло не так')


@user_private_router.callback_query(F.data.startswith('shipipaid_'))
async def paid_order(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    try:
        order = await orm_check_order_shop(session, order_shop_id=int(callback.data.split('_')[-1]))
        user = await orm_check_user(session=session, user_id=order.user_id)

        await bot.send_message(chat_id=bot.my_admins_list[-1],
                               text=f"#shipping\n\nПользователь оплатил заказ. Проверьте и измените статуc заказа.\n\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nЗаказ не оплачен.\nСумма к оплате - {round(order.amount, 0)} руб.\nПользователь - {user.user_name}",
                               reply_markup=get_callback_btns(btns={
                                   'Оплачено': f'shippaid_{order.id}',
                                   'Отменить': f'shipcancel_{order.id}',
                                   'Написать клиенту': f'shipmessage_{order.id}',
                               }))
        await callback.message.answer('В ближайщее время мы проверим оплату. И оплатим ваш сервис.')
    except Exception as e:
        await callback.message.answer('Что то пошло не так')
