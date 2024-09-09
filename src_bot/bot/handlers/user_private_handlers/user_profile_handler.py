from aiogram import F, types, Bot, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.main_menu import user_start_kb
from src_bot.database.orm_query.orm_users import orm_check_user_chat_id, orm_add_user

user_profile_router = Router()


class User(StatesGroup):
    chat_id = State()
    username = State()
    phone = State()
    first_name = State()
    last_name = State()
    confirm = State()


@user_profile_router.message(F.contact)
async def add_user(message: types.ContentType.CONTACT, session: AsyncSession, state: FSMContext):
    if message.contact is not None:
        chat_id = message.chat.id
        username = message.from_user.username
        phone = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name
        if await orm_check_user_chat_id(session, chat_id=chat_id) is None:
            await state.update_data(chat_id=chat_id, username=username, phone=phone, first_name=first_name,
                                    last_name=last_name)
            await state.set_state(User.confirm)
            await message.answer(
                f'Хотите зарегистрироваться с этими данными?\n\nТелефон - {phone},\nИмя - {first_name},\nФамилия - {last_name}',
                reply_markup=get_callback_btns(btns={'Подтвердить': 'confirm_sign_up', 'Отменить': 'cancel'}))
            # await orm_add_user(session, chat_id=chat_id, user_name=username, phone=phone, first_name=first_name,
            #                    last_name=last_name)
            # await message.answer('Вы зарегистрировались', reply_markup=user_start_kb)
        else:
            await message.answer('Вы уже зарегистрированы')
    else:
        await message.answer(
            'Для того чтобы продолжить пользоваться нашим сервисом, вам необходимо зарегистрироваться. Это необходимо для отслеживания и доставки ваших заказов. В профиле вы cможете отменить рассылку сообщений.',
            reply_markup=get_callback_btns(btns={'Зарегистрироваться': 'sign_up'}))


@user_profile_router.message(User.confirm, F.text)
async def confirm_sign_up(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer('Пожалуйста подтвердите регистрацию',
                         reply_markup=get_callback_btns(
                             btns={'Подтвердить': 'confirm_sign_up', 'Отменить': 'cancel'}))
    await state.set_state(User.confirm)


@user_profile_router.callback_query(User.confirm, F.data == 'confirm_sign_up')
async def confirm_sign_up(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.update_data(confirm=True)
    data = await state.get_data()
    try:
        await orm_add_user(session, data)
        await state.clear()
        await callback.message.answer('Вы зарегистрировались', reply_markup=user_start_kb)

    except Exception as e:
        await callback.message.answer('Что то пошло не так')
