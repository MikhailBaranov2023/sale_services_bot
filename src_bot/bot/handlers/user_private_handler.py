from aiogram.filters import CommandStart, StateFilter
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.main_menu import user_start_kb, cancel_kb
from src_bot.bot.keyboards.games_keyboards import games_kbd
from src_bot.bot.keyboards.shop_keyboard import shop_kbd, inline_kbd
from src_bot.bot.keyboards.profile_kbd import profile_kbd, register_kbd
from src_bot.database.orm_query.orm_users import orm_add_user, orm_check_user
from src_bot.database.orm_query.orm_order_shop import orm_create_order_shop, orm_check_order_shop, orm_get_order_shop

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start(message: types.Message, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await message.answer('Вы в админке')
    else:
        await message.answer('Я Работаю', reply_markup=user_start_kb)


@user_private_router.message(F.text == "Профиль", )
async def profile_keyboard(message: types.Message, bot: Bot, session: AsyncSession):
    if await orm_check_user(session, chat_id=message.from_user.id) is None:
        await message.answer('Для того чтобы продолжить вм необходимо зарегистрироваться.', reply_markup=register_kbd)
    else:
        await  message.answer(text=message.text, reply_markup=profile_kbd)


@user_private_router.message(F.text.lower() == "назад")
async def games_keyboard(message: types.Message):
    await message.answer('Главное меню', reply_markup=user_start_kb)


@user_private_router.message(F.text == "Доставка товаров")
async def shop(message: types.Message):
    await message.answer(
        text='Вы можете перейти на указанные cайты, выбрать товар и оставить заявку, После чего  с вами свяжется адиминистратор.',
        reply_markup=inline_kbd)


class OrderShop(StatesGroup):
    url = State()
    address = State()
    description = State()
    user_id = State()


@user_private_router.callback_query(F.data == 'make_order', StateFilter(None), )
async def shop(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        'Введите ссылку на товар. Если товаров несколько введите все ссылки в одном сообщении', reply_markup=cancel_kb)
    await state.set_state(OrderShop.url)


@user_private_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return None
    else:
        await state.clear()
    await message.answer('Действия отменены', reply_markup=user_start_kb)


@user_private_router.message(OrderShop.url, F.text)
async def add_url_order(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer('Введите адрес доставки')
    await state.set_state(OrderShop.address)


@user_private_router.message(OrderShop.address, F.text)
async def add_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите описания к заказу')
    await state.set_state(OrderShop.description)


@user_private_router.message(OrderShop.description, F.text)
async def add_description_order(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user = await orm_check_user(session, chat_id=message.from_user.id)
    await state.update_data(description=message.text, user_id=user.id)
    data = await state.get_data()
    try:
        order = await orm_create_order_shop(session, data)
        print(order)
        await message.answer('Ваш заказ принят. Скоро с вами свяжется администратор')
        print((await orm_get_order_shop(session, data)))
        # await bot.send_message(chat_id=bot.my_admins_list[0],
        #                        text=f'#SHOP')
        # await bot.send_message(chat_id=bot.my_admins_list[0],
        #                        text=f'#SHOP\nТовары - {(await orm_get_order_shop(session, data)).urls},\nОписание - {(await orm_get_order_shop(session, data)).description},\nАдрес доставки{order_shop.address}\nПользователь{user.user_name}')
    except Exception as e:
        message.answer('Что пошло не так. Пожалуйста свяжитесь с aдминистратором или попробуйте позже.')


class Services(StatesGroup):
    url = State()
    description = State()
    username = State()


@user_private_router.message(F.text == 'Оплата сервисов', StateFilter(None))
async def pay_services(message: types.Message, state: FSMContext):
    await message.answer('Введите ссылку на сервис который хотите оплатить', reply_markup=cancel_kb)
    await state.set_state(Services.url)


@user_private_router.message(Services.url, F.text)
async def add_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer('Введите описание')
    await state.set_state(Services.description)


@user_private_router.message(Services.description, F.text)
async def add_description(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    await state.update_data(description=message.text, username=message.from_user.username)
    data = await state.get_data()
    await message.answer(f'{data["url"]},{data["description"]}')
    await bot.send_message(chat_id=bot.my_admins_list[0],
                           text=f'SERVICES\nсервис - {data["url"]},\nописание - {data["description"]},\nпользователь - @{data["username"]}')
    await state.clear()


@user_private_router.message(F.text == "Игровые платформы")
async def games_keyboard(message: types.Message):
    await message.answer(text=message.text, reply_markup=games_kbd)


@user_private_router.message(F.text == "Зарегистрироваться")
async def add_user(message: types.Message, session: AsyncSession):
    chat_id = message.chat.id
    username = message.from_user.username
    if await orm_check_user(session, chat_id=chat_id) is None:
        await orm_add_user(session, chat_id=chat_id, user_name=username)
        await message.answer('Вы зарегистрировались', reply_markup=profile_kbd)
    else:
        await message.answer('Вы уже зарегистрированы')
