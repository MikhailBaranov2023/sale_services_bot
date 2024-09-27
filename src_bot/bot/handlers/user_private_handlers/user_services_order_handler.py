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
async def pay_services(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    current_state = await state.get_state()
    if current_state is None:
        if not await orm_check_user_chat_id(session, chat_id=callback.from_user.id) is None:
            await callback.message.answer(
                'Введите ссылку на сервис, который хотите оплатить.\n\nНапример:"https://www.airbnb.ru/rooms/33191989?adults=2&category_tag=Tag%3A8851&enable_m3_private_room=true&search_mode=flex_destinations_search"',
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
async def add_url(message: types.Message, state: FSMContext, ):
    await state.update_data(url=message.text)
    await message.answer(
        'Введите описание.\nЗдесь вы можете указать дополнительную информацию, необходимую для оплаты.\n\n Например, это может быты диапозон дат прибывания в отеле,который вы хотите забронировать, вид подписки - "годовая подписка на Netflix" и любая другая информация, относящаяся к оплате сервиса\n\nПомимо этого, вы можете написать сюда дополнительные вопросы которые хотели бы задать администратору')
    await state.set_state(Services.description)


@user_services_order_router.message(Services.description, F.text)
async def add_description(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user = await orm_check_user_chat_id(session, chat_id=message.from_user.id)
    await state.update_data(description=message.text, user_id=user.id, type='services')
    data = await state.get_data()
    try:
        await orm_create_order(session, data)
        await message.answer(
            'Ваша заявка принята.\nВ ближайшее время мы рассчитаем стоимость и пришлем вам реквизиты для оплаты.',
            reply_markup=user_start_kb)
        await state.clear()
    except Exception as e:
        print(e)
        await message.answer('Что пошло не так. Пожалуйста свяжитесь с aдминистратором или попробуйте позже.',
                             reply_markup=user_start_kb)
        await state.clear()
    try:
        order = await orm_get_order(session, data)
        await bot.send_message(chat_id=bot.my_admins_list[0],
                               text=f"#{order.type}\nCервис для оплаты -{order.url},\nОписание - {order.description}\nПользователь - @{user.user_name},\nЗаказ не оплачен.",
                               reply_markup=get_callback_btns(btns={
                                   'Расчитать': f'calculate_{order.id}',
                                   'Отменить': f'cancel_{order.id}',
                                   'Написать клиенту': f'message_{order.id}',
                               }))

    except Exception as e:
        print(e)
        await bot.send_message(chat_id=bot.my_admins_list[-1],
                               text='Новая заявка. Не удалось получить подробные данные заказа.')
