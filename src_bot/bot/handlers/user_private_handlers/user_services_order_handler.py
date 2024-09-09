from aiogram import F, types, Bot, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.main_menu import cancel_kb, user_start_kb
from src_bot.bot.keyboards.profile_kbd import register_kbd
from src_bot.database.orm_query.orm_order import orm_create_order, orm_get_order
from src_bot.database.orm_query.orm_users import orm_check_user_chat_id

user_services_order_router = Router()


class Services(StatesGroup):
    url = State()
    description = State()
    username = State()
    type = State()


@user_services_order_router.callback_query(F.data == 'services', StateFilter(None))
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


@user_services_order_router.message(Services.url, F.text)
async def add_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(
        'Введите описание.\nЗдесь вы можете указать дополнительную информацию необходимую для оплаты,\n\n Например, это может быты диапозон дат прибывания в отеле,который вы хотите забронировать, вид подписки "годовая подписка на Netflix" и любая диругая информация относящаяся к оплате сервиса\n\nПомимо этого, вы можете написать сюда дополнительные вопросы которые хотели бы задать администратору')
    await state.set_state(Services.description)


@user_services_order_router.message(Services.description, F.text)
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
