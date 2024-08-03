from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.admin_shipping_kb import shipping_kbd
from src_bot.database.orm_query.orm_order_shop import orm_get_all_current_order_shop, orm_get_all_cancel_order_shop, \
    orm_get_all_complete_order_shop, orm_update_order_shop, orm_check_order_shop
from src_bot.database.orm_query.orm_users import orm_check_user
from src_bot.bot.keyboards.inline import get_callback_btns

admin_private_router = Router()


@admin_private_router.message(F.text == 'Доставка')
async def services(message: types.Message, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await message.answer(message.text, reply_markup=shipping_kbd)
    else:
        await message.answer(message.text)


@admin_private_router.message(F.text == 'SHOP Заказы ожидающие оплаты')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        # try:
        orders = await orm_get_all_current_order_shop(session)
        for order in orders:
            user = await orm_check_user(session, order.user_id)
            if user is None:
                if order.payment_status is True:

                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ оплачен на сумму - {round(order.amount, 2)}руб,\nТрек-номер - {order.track_number}",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'payment_{order.id}',
                            'Отменить': f'payment_{order.id}',
                            'Добавить трек код': f'track_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ не оплачен,\nТрек-номер - {order.track_number}",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'payment_{order.id}',
                            'Отменить': f'payment_{order.id}',
                            'Добавить трек код': f'track_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))
            else:
                if order.payment_status is True:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ оплачен на сумму - {round(order.amount, 2)}руб,\nТрек-номер - {order.track_number}",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'payment_{order.id}',
                            'Отменить': f'payment_{order.id}',
                            'Добавить трек код': f'track_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ не оплачен,\nТрек-номер - {order.track_number}",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'payment_{order.id}',
                            'Отменить': f'payment_{order.id}',
                            'Добавить трек код': f'track_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))
            count += 1
        if count == 0:
            await message.answer(
                text="Нет заказов")
    # except Exception as e:
    #     await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@admin_private_router.message(F.text == 'SHOP Отмененные заказы')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_all_cancel_order_shop(session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nСтатус оплаты - {order.payment_status},\nТрек-номер - {order.track_number}")
                else:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{order.user.user_name},\nСтатус оплаты - {order.payment_status},\nТрек-номер - {order.track_number}")
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет отмененных заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@admin_private_router.message(F.text == 'SHOP Исполненные заказы')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_all_complete_order_shop(session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nСтатус оплаты - {order.payment_status},\nТрек-номер - {order.track_number}")

                else:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nСтатус оплаты - {order.payment_status},\nТрек-номер - {order.track_number}")
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет исполненных заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


class Amount(StatesGroup):
    order_shop_id = State()
    amount = State()


@admin_private_router.callback_query(F.data.startswith('payment_'), StateFilter(None))
async def change_payment_status(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    if callback.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(Amount.order_shop_id)
            await state.update_data(order_shop_id=callback.data.split('_')[-1])
            await state.set_state(Amount.amount)
            await callback.message.answer('Введите сумму заказа')


@admin_private_router.message(Amount.amount, F.text)
async def add_amount_for_order_shop(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.update_data(amount=message.text)
    data = await state.get_data()
    try:
        await orm_update_order_shop(session=session, amount=data['amount'], order_shop_id=int(data['order_shop_id']))
        await message.answer('Сумма заказа и статус оплаты обновлены')
        await state.clear()
        order = await orm_check_order_shop(session=session, order_shop_id=int(data['order_shop_id']))
        try:
            user = await orm_check_user(user_id=order.user_id, session=session)
            await bot.send_message(chat_id=user.chat_id,
                                   text=f'Общая сумма к оплате с комиссией-{round(order.amount, 2)}руб\nВы можете оплать СБП по номеру +79998502717(Райфайзенбанк), либо по номеру карты', )
        except Exception as e:
            pass
    except Exception as e:
        await message.answer('Что то пошло не так.')
        await state.clear()


class Message(StatesGroup):
    user_id = State()
    message = State()


@admin_private_router.callback_query(F.data.startswith('message_'), StateFilter(None))
async def write_to_user(callback: types.CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession):
    if callback.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(Message.user_id)
            order = await orm_check_order_shop(session=session, order_shop_id=int(callback.data.split('_')[-1]))
            await state.update_data(user_id=order.user_id)
            await state.set_state(Message.message)
            await callback.message.answer('Введите ваше сообщение')


@admin_private_router.message(Message.message, F.text)
async def add_message(message: types.Message, session: AsyncSession, bot: Bot, state: FSMContext):
    await state.update_data(message=message.text)
    data = await state.get_data()
    user = await orm_check_user(user_id=data['user_id'], session=session)
    chat_id = user.chat_id
    try:
        await bot.send_message(chat_id=chat_id,
                               text=f"Администратор отправил вам сообщение:\n'{data['message']}'.\nДля того чтобы ответить свяжитесь с администратором @problemaprod")
        await message.answer('Сообщение отправлено')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer('Что то пошло не так')
