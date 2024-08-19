from aiogram.filters import CommandStart, StateFilter
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.main_menu import user_start_kb, cancel_kb, admin_start_kb
from src_bot.bot.keyboards.games_keyboards import games_kbd
from src_bot.bot.keyboards.shop_keyboard import inline_kbd, inline_services_kbd
from src_bot.bot.keyboards.profile_kbd import profile_kbd, register_kbd
from src_bot.database.orm_query.orm_users import orm_add_user, orm_check_user_chat_id
from src_bot.database.orm_query.orm_order_shop import orm_create_order_shop, orm_check_order_shop, orm_get_order_shop
from src_bot.database.orm_query.orm_order import orm_create_order, orm_get_order
from src_bot.database.orm_query.orm_product import orm_get_product_shop, orm_get_product_services
from src_bot.bot.keyboards.inline import get_inlineMix_btns
from src_bot.bot.handlers.user_private_handlers.user_game_handler import game_menu_router

user_private_router = Router()
user_private_router.include_routers(game_menu_router, )


@user_private_router.message(F.text == 'user')
async def user_menu(message: types.Message, bot: Bot, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        if message.from_user.id in bot.my_admins_list:
            await message.answer('Меню пользователя', reply_markup=user_start_kb)


@user_private_router.message(CommandStart())
async def start(message: types.Message, bot: Bot, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        if message.from_user.id in bot.my_admins_list:
            await message.answer('Вы в админке', reply_markup=admin_start_kb)
        else:
            if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
                await message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                     reply_markup=register_kbd)
            else:
                await message.answer('Рады видеть вас снова', reply_markup=user_start_kb)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_private_router.message(F.text == "Профиль", )
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


@user_private_router.message(F.text == "Главное меню")
async def games_keyboard(message: types.Message, bot: Bot, session: AsyncSession):
    if message.from_user.id in bot.my_admins_list:
        await message.answer('Вы в админке', reply_markup=admin_start_kb)
    else:
        if await orm_check_user_chat_id(session, chat_id=message.from_user.id) is None:
            await message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                 reply_markup=register_kbd)
        else:
            await message.answer(message.text, reply_markup=user_start_kb)


@user_private_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(message: types.Message, state: FSMContext, bot: Bot) -> None:
    current_state = await state.get_state()
    if current_state is None:
        if message.from_user.id in bot.my_admins_list:
            await message.answer(message.text, reply_markup=admin_start_kb)
        else:
            await message.answer(message.text, reply_markup=user_start_kb)
    else:
        await state.clear()
        if message.from_user.id in bot.my_admins_list:
            await message.answer('Действия отменены', reply_markup=admin_start_kb)
        else:
            await message.answer('Действия отменены', reply_markup=user_start_kb)


@user_private_router.message(F.text == "Доставка товаров")
async def shop_add_product(message: types.Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        product = await orm_get_product_shop(session=session)

        await message.answer_photo(photo=product.image, caption=f"{product.title}\n\n{product.description}",
                                   reply_markup=inline_kbd)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


class OrderShop(StatesGroup):
    url = State()
    address = State()
    description = State()
    user_id = State()
    user_name = State()


@user_private_router.callback_query(F.data == 'make_order', StateFilter(None))
async def shop_make_order(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        if await orm_check_user_chat_id(session, chat_id=callback.from_user.id) is not None:
            await callback.message.answer(
                'Введите ссылку на товар\товары.\nТовары могут быть с разных платформ в неограниченном количестве.\n В случае если товаров несколько введите несолько ссылок в формате\n "https://www.adidas.pt/sapatilhas-campus-00s/HQ8707.html?forceSelSize=HQ8707_620\n\nhttps://www.adidas.pt/sapatilhas-ny-90/JI1893.html?pr=cart_rr&slot=4&rec=mt"',
                reply_markup=cancel_kb)
            await state.set_state(OrderShop.url)
        else:
            await callback.message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                          reply_markup=register_kbd)
            await state.clear()
    else:
        await state.clear()
        await callback.message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_private_router.message(OrderShop.url, F.text)
async def add_url_order(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(
        'Введите адрес.\nВведенный вами адрес будет указан при отправке товара, пожалуйста убедитесь что вы ввели адрес в формате:\nРоссия, Москва, Тверская улица, д.2, кв.1, 109012')
    await state.set_state(OrderShop.address)


@user_private_router.message(OrderShop.address, F.text)
async def add_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(
        'Введите описание.\nЗдесь вы можете указать дополнительную информацию необходимую для оплаты,\n\n Например, это может быты размер, желаемый цвет, промокод и тд.\n\nПомимо этого, вы можете написать сюда дополнительные вопросы связанные с конкретным заказом которые хотели бы задать администратору')
    await state.set_state(OrderShop.description)


@user_private_router.message(OrderShop.description, F.text)
async def add_description_order(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user = await orm_check_user_chat_id(session, chat_id=message.from_user.id)
    await state.update_data(description=message.text, user_id=user.id)
    data = await state.get_data()
    try:
        await orm_create_order_shop(session, data)
        await message.answer(
            'Ваша заявка принята.\nВ близжайщее время мы рассчитаем стоимость и пришлем вам реквизиты для оплаты.',
            reply_markup=user_start_kb)
        order = await orm_get_order_shop(session, data)
        await bot.send_message(chat_id=bot.my_admins_list[0],
                               text=f"#SHOP\nНОВЫЙ ЗАКАЗ\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ не оплачен.",
                               reply_markup=get_callback_btns(btns={
                                   'Оплачено': f'payment_{order.id}',
                                   'Отменить': f'cancel_{order.id}',
                                   'Написать пользователю': f'message_{order.id}',
                               }))

        await state.clear()
    except Exception as e:
        await message.answer('Что пошло не так. Пожалуйста свяжитесь с aдминистратором или попробуйте позже.',
                             reply_markup=user_start_kb)
        await state.clear()


@user_private_router.message(F.text == 'Оплата сервисов', StateFilter(None))
async def pay_services(message: types.Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        product = await orm_get_product_services(session=session)

        await message.answer_photo(photo=product.image,
                                   caption=f"{product.title}\n\nКомиссия 5%. Минимальная от {round(product.price, 2)}руб.\n\n{product.description}",
                                   reply_markup=inline_services_kbd)
    else:
        await state.clear()
        await message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


class Services(StatesGroup):
    url = State()
    description = State()
    username = State()
    type = State()


@user_private_router.callback_query(F.data == 'services', StateFilter(None))
async def pay_services(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        if not await orm_check_user_chat_id(session, chat_id=callback.from_user.id) is None:
            await callback.message.answer(
                'Введите ссылку на сервис который хотите оплатить.\n\nНапример:"https://www.airbnb.ru/rooms/33191989?adults=2&category_tag=Tag%3A8851&enable_m3_private_room=true&search_mode=flex_destinations_search"',
                reply_markup=cancel_kb)
            await state.set_state(Services.url)
        else:
            await callback.message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                          reply_markup=register_kbd)
            await state.clear()
    else:
        await state.clear()
        await callback.message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_private_router.message(Services.url, F.text)
async def add_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(
        'Введите описание.\nЗдесь вы можете указать дополнительную информацию необходимую для оплаты,\n\n Например, это может быты диапозон дат прибывания в отеле,который вы хотите забронировать, вид подписки "годовая подписка на Netflix" и любая диругая информация относящаяся к оплате сервиса\n\nПомимо этого, вы можете написать сюда дополнительные вопросы которые хотели бы задать администратору')
    await state.set_state(Services.description)


@user_private_router.message(Services.description, F.text)
async def add_description(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user = await orm_check_user_chat_id(session, chat_id=message.from_user.id)
    await state.update_data(description=message.text, user_id=user.id, type='services')
    data = await state.get_data()
    try:
        await orm_create_order(session, data)
        await message.answer(
            'Ваша заявка принята.\nВ близжайщее время мы рассчитаем стоимость и пришлем вам реквизиты для оплаты.',
            reply_markup=user_start_kb)
        order = await orm_get_order(session, data)
        await bot.send_message(chat_id=bot.my_admins_list[0],
                               text=f'#SERVICES\nСервис - {order.url},\nописание - {order.description},\nпользователь - @{user.user_name}')
        await state.clear()
    except Exception as e:
        await message.answer('Что пошло не так. Пожалуйста свяжитесь с aдминистратором или попробуйте позже.',
                             reply_markup=user_start_kb)
        await state.clear()


@user_private_router.message(F.text == "Игровые платформы")
async def games_keyboard(message: types.Message):
    await message.answer(text=message.text, reply_markup=games_kbd)


@user_private_router.message(F.contact or F.data == 'sign_up')
async def add_user(message: types.ContentType.CONTACT, session: AsyncSession):
    if message.contact is not None:
        chat_id = message.chat.id
        username = message.from_user.username
        phone = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name
        if await orm_check_user_chat_id(session, chat_id=chat_id) is None:
            await orm_add_user(session, chat_id=chat_id, user_name=username, phone=phone, first_name=first_name,
                               last_name=last_name)
            await message.answer('Вы зарегистрировались', reply_markup=user_start_kb)
        else:
            await message.answer('Вы уже зарегистрированы')
    else:
        await message.answer(
            'Для того чтобы продолжить пользоваться нашим сервисом, вам необходимо зарегистрироваться. Это необходимо для отслеживания и доставки ваших заказов. В профиле вы cможете отменить рассылку сообщений.',
            reply_markup=get_callback_btns(btns={'Зарегистрироваться': 'sign_up'}))
