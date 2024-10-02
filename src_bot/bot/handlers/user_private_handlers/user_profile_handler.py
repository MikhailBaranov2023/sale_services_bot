from aiogram import F, types, Bot, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.main_menu import user_start_kb
from src_bot.database.orm_query.orm_order import orm_user_orders
from src_bot.database.orm_query.orm_order_shop import orm_user_shop_orders
from src_bot.database.orm_query.orm_users import orm_check_user_chat_id, orm_add_user
from src_bot.bot.keyboards.profile_kbd import my_orders_kbd

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
        else:
            await message.answer('Вы уже зарегистрированы')
    else:
        await message.answer(
            'Для того чтобы продолжить пользоваться нашим сервисом, вам необходимо зарегистрироваться. Это необходимо для отслеживания и доставки ваших заказов. В профиле вы cможете отменить рассылку сообщений.',
            reply_markup=get_callback_btns(btns={'Зарегистрироваться': 'sign_up'}))


@user_profile_router.message(User.confirm, F.text)
async def confirm_sign_up(message: types.Message, state: FSMContext):
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
        await callback.message.answer('Вы успешно зарегистрировались.\n\nТеперь вам доступны все фунцкции этого бота.', reply_markup=user_start_kb)

    except Exception as e:
        await callback.message.answer('Что то пошло не так')


@user_profile_router.message(F.text == 'Мои заказы')
async def my_orders(message: types.Message):
    await message.answer(message.text, reply_markup=my_orders_kbd)


@user_profile_router.message(F.text == 'Мои заказы в доставке')
async def my_ship_orders(message: types.Message, session: AsyncSession):
    user = await orm_check_user_chat_id(session, chat_id=message.chat.id)
    orders = await orm_user_shop_orders(session, user_id=user.id)
    count = 0
    for order in orders:
        if order.cancel_status is True or order.order_status is True:
            continue
        elif order.amount is None:
            await message.answer(
                text=f"Заказ ожидает рассчета. В близжайщее время с вами свяжется администратор.\n\nДетали заказа:\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\n\nЗаказ не оплачен.",
                reply_markup=get_callback_btns(btns={
                    'Отменить': f'shipcancel_{order.id}',
                    'Cвязаться с администратором': 'admin_message',
                }))
            count += 1
        elif order.amount is not None:
            if order.payment_status is False:
                await message.answer(
                    text=f"Заказ ожидает оплаты.\n\nОбщая сумма к оплате с комиссией-{round(order.amount, 2)}руб\n\nВы можете оплатить через СБП по номеру +79998502717(Райфайзенбанк), либо по номеру карты.\n\nДетали заказа:\n\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nЗаказ не оплачен.",
                    reply_markup=get_callback_btns(btns={
                        'Отменить': f'shipcancel_{order.id}',
                        'Cвязаться с администратором': 'admin_message',
                    }))
                count += 1
            elif order.payment_status is True:
                if order.track_number is None:
                    await message.answer(
                        text=f"Мы ждем ваш заказ.\n\nКогда мы отправим ваш заказ, вы получите сообщение и трек-код по которому можно будет отслеживать ваш заказ.\nПо другим вопросам можете обратиться к администратору.\n\nДетали заказа:\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nсумма заказа-{round(order.amount, 2)}руб",
                        reply_markup=get_callback_btns(btns={
                            'Cвязаться с администратором': 'admin_message',
                        }))
                    count += 1

                elif order.track_number is not None:
                    await message.answer(
                        text=f"Ваш заказ уже отправлен вам.\n\nВы можете отследить его на сайте 'https:'\n\nТрек номер - {order.track_number}\n\nДетали заказа:\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nсумма заказа-{round(order.amount, 2)}руб",
                        reply_markup=get_callback_btns(btns={
                            'Cвязаться с администратором': 'admin_message',
                        }))
                    count += 1
    if count == 0:
        await message.answer('У вас нет текущих заказов')


@user_profile_router.message(F.text == 'Заказы по оплате сервисов')
async def my_services_orders(message: types.Message, session: AsyncSession):
    try:
        user = await orm_check_user_chat_id(session, chat_id=message.chat.id)
        orders = await orm_user_orders(session, user_id=user.id)
        count = 0
        for order in orders:
            if order.cancel_status is True or order.order_status is True:
                continue
            elif order.amount is None:
                await message.answer(
                    text=f"Заказ ожидает рассчета. В близжайщее время с вами свяжется администратор.\n\nДетали заказа:\nСервис для оплаты - {order.url},\nОписание - {order.description},\n\nЗаказ не оплачен.",
                    reply_markup=get_callback_btns(btns={
                        'Отменить': f'cancel_{order.id}',
                        'Cвязаться с администратором': 'admin_message',
                    }))
                count += 1
            elif order.amount is not None:
                if order.payment_status is False:
                    await message.answer(
                        text=f"Заказ ожидает оплаты.\n\nОбщая сумма к оплате с комиссией-{round(order.amount, 2)}руб\n\nВы можете оплатить через СБП по номеру +79998502717(Райфайзенбанк), либо по номеру карты.\n\nДетали заказа:\nСервис для оплаты - {order.url},\nОписание - {order.description},\n\nЗаказ не оплачен.",
                        reply_markup=get_callback_btns(btns={
                            'Отменить': f'cancel_{order.id}',
                            'Cвязаться с администратором': 'admin_message',
                        }))
                    count += 1
                elif order.payment_status is True:
                    await message.answer(
                        text=f"Заказ оплачен\n\nВ ближайщее время мы оплатим указанный вами сервис и пришлем вам всю необходимую информацию\n\nЕсли у вас есть вопросы вы можете связаться с администратором.\n\nДетали заказа:\nСервис для оплаты - {order.url},\nОписание - {order.description},\n\n",
                        reply_markup=get_callback_btns(btns={
                            'Cвязаться с администратором': 'admin_message',
                        }))
                    count += 1
        if count == 0:
            await message.answer('У вас нет текущих заказов')
    except Exception as e:
        print(e)
        await message.answer('Что то пошло не так. Пожалуйста попробуйте позже.')
