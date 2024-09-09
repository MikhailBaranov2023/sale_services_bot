from aiogram import Bot, Dispatcher, types, Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.main_menu import admin_start_kb
from src_bot.database.orm_query.orm_order import orm_update_amount_order, orm_check_order, \
    orm_cancel_order, orm_get_cancel_orders, orm_get_services_order_wait_complete, orm_complete_order, \
    orm_order_update_payment_status
from src_bot.database.orm_query.orm_product import orm_create_product
from src_bot.database.orm_query.orm_users import orm_check_user

services_router = Router()


# class ServicesProduct(StatesGroup):
#     image = State()
#     title = State()
#     price = State()
#     description = State()
#     store_section = State()
#
#
# @services_router.message(F.text == 'SERVICES Добавить товар', StateFilter(None))
# async def add_services_product(message: types.Message, bot: Bot, state: FSMContext):
#     if message.from_user.id in bot.my_admins_list:
#         current_state = await state.get_state()
#         if current_state is None:
#             await state.set_state(ServicesProduct.image)
#             await message.answer('Добавьте фотографию')
#         else:
#             await message.answer('Действия отменены', reply_markup=admin_start_kb)
#             await state.clear()
#
#
# @services_router.message(ServicesProduct.image, F.text)
# async def check_photo_services(message: types.Message, state: FSMContext):
#     if message.text:
#         await message.answer('Это не фото, пожалуйста добавьте фото')
#         await state.set_state(ServicesProduct.image)
#
#
# @services_router.message(ServicesProduct.image, F.photo)
# async def add_image_services(message: types.Message, state: FSMContext):
#     image = message.photo[-1].file_id
#     print(image)
#     await state.update_data(image=image)
#     await state.set_state(ServicesProduct.title)
#     await message.answer('Введите название товара')
#
#
# @services_router.message(ServicesProduct.title, F.text)
# async def add_title_services(message: types.Message, state: FSMContext):
#     await state.update_data(title=message.text)
#     await state.set_state(ServicesProduct.price)
#     await message.answer('Введите цену')
#
#
# @services_router.message(ServicesProduct.price, F.text)
# async def add_price_services(message: types.Message, state: FSMContext):
#     await state.update_data(price=float(message.text))
#     await state.set_state(ServicesProduct.description)
#     await message.answer('Введите описание')
#
#
# @services_router.message(ServicesProduct.description, F.text)
# async def add_description_services(message: types.Message, state: FSMContext, session: AsyncSession):
#     await state.update_data(description=message.text, store_section='Services')
#     data = await state.get_data()
#     try:
#         await orm_create_product(session=session, data=data)
#         await state.clear()
#         await message.answer('Продукт добавлен')
#     except Exception as e:
#         await state.clear()
#         await message.answer('Что то пошло не так')


@services_router.message(F.text == 'SERVICES Отмененные заказы')
async def all_cancel_services_orders(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_cancel_orders(session=session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#SERVICES\nCервис для оплаты - {order.url},\nОписание - {order.description},\nПользователь удален,\nЗаказ отменен",
                        reply_markup=get_callback_btns(btns={
                            'Написать пользователю': f'SERVICESmessage_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#SERVICES\nCервис для оплаты - {order.url},\nОписание - {order.description}\nПользователь - @{user.user_name},\nЗаказ отменен.",
                        reply_markup=get_callback_btns(btns={
                            'Написать пользователю': f'SERVICESmessage_{order.id}',
                        }))
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет заказов ожидающих оплаты")
        except Exception as e:
            await message.answer('Что то пошло не так')


@services_router.message(F.text == 'SERVICES Оплаченные заказы, ожидающие исполнения')
async def all_shop_orders_wait_complete(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_services_order_wait_complete(session=session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#SERVICES\nCервис для оплаты-{order.url},\nОписание - {order.description},\nПользователь удален,\nЗаказ оплачен",
                        reply_markup=get_callback_btns(btns={
                            'Отменить': f'SERVICEScancel_{order.id}', \
                            'Исполнено': f'SERVICEcomplete_{order.id}',
                            'Написать пользователю': f'SERVICESmessage_{order.id}',
                        }))

                else:
                    await message.answer(
                        text=f"#SERVICES\nCервис для оплаты-{order.url},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ оплачен,",
                        reply_markup=get_callback_btns(btns={
                            'Отменить': f'SERVICEScancel_{order.id}',
                            'Исполнено': f'SERVICEcomplete_{order.id}',
                            'Написать пользователю': f'SERVICESmessage_{order.id}',
                        }))
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет заказов заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


class AmountServices(StatesGroup):
    order_id = State()
    amount = State()


@services_router.callback_query(F.data.startswith('calculate_'), StateFilter(None))
async def change_payment_status(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    if callback.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(AmountServices.order_id)
            await state.update_data(order_id=callback.data.split('_')[-1])
            await state.set_state(AmountServices.amount)
            await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.from_user.id)
            await callback.message.answer('Введите сумму заказа')


@services_router.message(AmountServices.amount, F.text)
async def add_amount_for_order_shop(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.update_data(amount=message.text)
    data = await state.get_data()
    try:
        await orm_update_amount_order(session=session, amount=data['amount'], order_id=int(data['order_id']))
        await message.answer('Сумма заказа обновлена')
        await state.clear()
        order = await orm_check_order(session=session, order_id=int(data['order_id']))
        await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)

        try:
            user = await orm_check_user(user_id=order.user_id, session=session)
            await bot.send_message(chat_id=user.chat_id,
                                   text=f'Общая сумма к оплате с комиссией-{round(order.amount, 2)}руб\n\nВы можете оплатить через СБП по номеру +79998502717(Райфайзенбанк), либо по номеру карты')
        except Exception as e:
            pass
    except Exception as e:
        await message.answer('Что то пошло не так.')
        await state.clear()


class MessageOrder(StatesGroup):
    user_id = State()
    message = State()


@services_router.callback_query(F.data.startswith('message_'), StateFilter(None))
async def write_to_user(callback: types.CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession):
    if callback.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(MessageOrder.user_id)
            order = await orm_check_order(session=session, order_id=int(callback.data.split('_')[-1]))
            await state.update_data(user_id=order.user_id)
            await state.set_state(MessageOrder.message)
            await callback.message.answer('Введите ваше сообщение')


@services_router.message(MessageOrder.message, F.text)
async def add_message(message: types.Message, session: AsyncSession, bot: Bot, state: FSMContext):
    await state.update_data(message=message.text)
    data = await state.get_data()
    user = await orm_check_user(user_id=data['user_id'], session=session)
    chat_id = user.chat_id
    try:
        await bot.send_message(chat_id=chat_id,
                               text=f"Администратор отправил вам сообщение:\n\n'{data['message']}'.\n\nДля того чтобы ответить свяжитесь с администратором @problemaprod")
        await message.answer('Сообщение отправлено')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer('Что то пошло не так')


@services_router.callback_query(F.data.startswith('paid_'))
async def paid_order(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    try:
        await orm_order_update_payment_status(session=session, order_id=int(callback.data.split('_')[-1]))
        await callback.message.answer('Статус оплаты изменен')
        order = await orm_check_order(session=session, order_id=int(callback.data.split('_')[-1]))
        user = await orm_check_user(session=session, user_id=order.user_id)
        chat_id = user.chat_id
        await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.from_user.id)
        await bot.send_message(chat_id=chat_id,
                               text=f'Выша оплата принята.\nВ ближайщее время мы оплатим нужный сервис и пришлем вам всю необходимую информацию.\nПо другим вопросам можете обратиться к администратору @problemaprod .')
    except Exception as e:
        await callback.message.answer('Что то пошло не так')


@services_router.callback_query(F.data.startswith('cancel_'))
async def cancel_order(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    try:
        await orm_cancel_order(session=session, order_id=int(callback.data.split('_')[-1]))
        await callback.message.answer('Заявка отменена')
        order = await orm_check_order(session=session, order_id=int(callback.data.split('_')[-1]))
        user = await orm_check_user(session=session, user_id=order.user_id)
        chat_id = user.chat_id
        await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.from_user.id)
        await bot.send_message(chat_id=chat_id,
                               text=f'Ваша завка по оплате сервиса:"{order.url}" отменена.\n\nЕсли хотите повторить, пожалуйста создайте новую заявку')
    except Exception as e:
        await callback.message.answer('Что то пошло не так')


@services_router.callback_query(F.data.startswith('compelete_'))
async def complete_order(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    if callback.from_user.id in bot.my_admins_list:
        try:
            await orm_complete_order(session=session, order_id=int(callback.data.split('_')[-1]))
            await callback.message.answer('Заявка исполнена')
            order = await orm_check_order(session=session, order_id=int(callback.data.split('_')[-1]))
            user = await orm_check_user(session=session, user_id=order.user_id)
            chat_id = user.chat_id
            await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.from_user.id)

            await bot.send_message(chat_id=chat_id,
                                   text=f'Ваша завка по оплате сервиса:"{order.url}" исполнена.\n\n Будем рад видеть вас снова.')
        except Exception as e:
            await callback.message.answer('Что то пошло не так')
