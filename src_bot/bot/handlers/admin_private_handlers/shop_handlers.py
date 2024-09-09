from aiogram import Bot, Dispatcher, types, Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src_bot.database.orm_query.orm_order_shop import orm_get_all_shop_orders_awaiting_calculate, \
    orm_get_all_cancel_order_shop, \
    orm_update_order_shop_amount, orm_check_order_shop, orm_cancel_order_shop, orm_get_order_shop_wait_shipping, \
    orm_add_track_code, orm_get_order_shop_wait_complete, orm_complete_order_shop, orm_order_shop_update_payment_status
from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.database.orm_query.orm_product import orm_create_product
from src_bot.database.orm_query.orm_users import orm_check_user

shop_router = Router()


@shop_router.message(F.text == 'SHOP Заказы ожидающие рассчета')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_all_shop_orders_awaiting_calculate(session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#SHOP\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ не оплачен,\nТрек-номер - {order.track_number}",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'payment_{order.id}',
                            'Отменить': f'cancel_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))
                else:

                    await message.answer(
                        text=f"#SHOP\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ не оплачен,\nТрек-номер - {order.track_number}",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'payment_{order.id}',
                            'Отменить': f'cancel_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@shop_router.message(F.text == 'SHOP Отмененные заказы')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        # try:
        orders = await orm_get_all_cancel_order_shop(session)
        for order in orders:
            user = await orm_check_user(session, order.user_id)
            if user is None:
                await message.answer(
                    text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ отменен")
            else:
                await message.answer(
                    text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ отменен")
            count += 1
        if count == 0:
            await message.answer(
                text="Нет отмененных заказов")
    # except Exception as e:
    #     await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@shop_router.message(F.text == 'SHOP Оплаченные заказы, ожидающие доставки')
async def all_shop_orders_wait_shipping(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_order_shop_wait_shipping(session=session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ оплачен",
                        reply_markup=get_callback_btns(btns={
                            'Отменить': f'cancel_{order.id}',
                            'Добавить трек код': f'track_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))

                else:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ оплачен,",
                        reply_markup=get_callback_btns(btns={
                            'Отменить': f'cancel_{order.id}',
                            'Добавить трек код': f'track_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет заказов заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@shop_router.message(F.text == 'SHOP Заказы в доставке')
async def all_shop_orders_wait_complete(message: types.Message, session: AsyncSession, bot: Bot):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_order_shop_wait_complete(session=session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ оплачен",
                        reply_markup=get_callback_btns(btns={
                            'Исполнено': f'complete_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))

                else:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ оплачен,",
                        reply_markup=get_callback_btns(btns={
                            'Исполнено': f'complete_{order.id}',
                            'Написать пользователю': f'message_{order.id}',
                        }))
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет заказов заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


class TrackNumber(StatesGroup):
    order_shop_id = State()
    track_number = State()


@shop_router.callback_query(F.data.startswith('track_'), StateFilter(None))
async def add_track_number(callback: types.CallbackQuery, bot: Bot, state: F):
    if callback.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(TrackNumber.order_shop_id)
            await state.update_data(order_shop_id=callback.data.split('_')[-1])
            await state.set_state(TrackNumber.track_number)
            await callback.message.answer('Введите трек код')


@shop_router.message(TrackNumber.track_number, F.text)
async def add_track_number_order_shop(message: types.Message, session: AsyncSession, bot: Bot, state: FSMContext):
    await state.update_data(track_number=message.text)
    data = await state.get_data()
    try:
        if await orm_add_track_code(session=session, track_number=data['track_number'],
                                    order_shop_id=int(data['order_shop_id'])) is True:
            order = await orm_check_order_shop(order_shop_id=int(data['order_shop_id']), session=session)
            user = await orm_check_user(session, order.user_id)
            user_chat_id = user.chat_id
            await bot.send_message(chat_id=user_chat_id,
                                   text=f'Ваш заказ : {order.url} отправлен.\nВы можете отслеживать статус доставки на сайте - \n Ваш трек код - {order.track_number}')
            await message.answer('Трек код добавлен')
            await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)

        else:
            await message.answer('Заказу уже присвоен трек код.')
            await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)

    except Exception as e:
        await message.answer('что то пошло не так')


class Amount(StatesGroup):
    order_shop_id = State()
    amount = State()


@shop_router.callback_query(F.data.startswith('shipcalculate_'), StateFilter(None))
async def change_payment_status(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    if callback.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(Amount.order_shop_id)
            await state.update_data(order_shop_id=callback.data.split('_')[-1])
            await state.set_state(Amount.amount)
            await callback.message.answer('Введите сумму заказа')


@shop_router.message(Amount.amount, F.text)
async def add_amount_for_order_shop(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.update_data(amount=message.text)
    data = await state.get_data()
    try:
        await orm_update_order_shop_amount(session=session, amount=data['amount'],
                                           order_shop_id=int(data['order_shop_id']))
        await message.answer('Сумма заказа обновлена')
        await state.clear()
        order = await orm_check_order_shop(session=session, order_shop_id=int(data['order_shop_id']))
        await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)

        try:
            user = await orm_check_user(user_id=order.user_id, session=session)
            await bot.send_message(chat_id=user.chat_id,
                                   text=f'Общая сумма к оплате с комиссией-{round(order.amount, 2)}руб\nВы можете оплатить через СБП по номеру +79998502717(Райфайзенбанк), либо по номеру карты')
        except Exception as e:
            pass
    except Exception as e:
        await message.answer('Что то пошло не так.')
        await state.clear()


@shop_router.callback_query(F.data.startswith('complete_'))
async def complete_shop_order(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    if callback.from_user.id in bot.my_admins_list:
        try:
            await orm_complete_order_shop(session=session, order_shop_id=int(callback.data.split('_')[-1]))
            await callback.message.answer('Заявка исполнена')
            order = await orm_check_order_shop(session=session, order_shop_id=int(callback.data.split('_')[-1]))
            user = await orm_check_user(session=session, user_id=order.user_id)
            chat_id = user.chat_id
            await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.from_user.id)

            await bot.send_message(chat_id=chat_id,
                                   text=f'Исполнено\n\nВаша заказ {order.url} был доставлен.\n\nБудем рад видеть вас снова.')
        except Exception as e:
            await callback.message.answer('Что то пошло не так')


@shop_router.callback_query(F.data.startswith('shipcancel_'))
async def cancel_shop_order(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    try:
        await orm_cancel_order_shop(session=session, order_shop_id=int(callback.data.split('_')[-1]))
        await callback.message.answer('Заявка отменена')
        order = await orm_check_order_shop(session=session, order_shop_id=int(callback.data.split('_')[-1]))
        user = await orm_check_user(session=session, user_id=order.user_id)
        chat_id = user.chat_id
        await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.from_user.id)
        await bot.send_message(chat_id=chat_id,
                               text=f'Ваша завка на доставку товаров отменена.\n\nТовары для доставки - {order.url}\n\nЕсли хотите повторить, пожалуйста создайте новую заявку')
    except Exception as e:
        await callback.message.answer('Что то пошло не так')


@shop_router.callback_query(F.data.startswith('shippaid'), StateFilter(None))
async def paid_shop_orders(callback: types.CallbackQuery, bot: Bot, session: AsyncSession):
    try:
        await orm_order_shop_update_payment_status(session=session, order_shop_id=int(callback.data.split('_')[-1]))
        await callback.message.answer('Статус оплаты изменен')
        await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.from_user.id)
        order = await orm_check_order_shop(session=session, order_shop_id=int(callback.data.split('_')[-1]))
        user = await orm_check_user(session=session, user_id=order.user_id)
        chat_id = user.chat_id
        await bot.send_message(chat_id=chat_id,
                               text=f'Выша оплата принята.\n\nВ ближайщее время мы оплатим ваши товары и пришлем вам всю необходимую информацию.\n\nКогда мы отправим ваш заказ, вы получите сообщение и трек-код по которому можно будет отслеживать ваш заказ.\nПо другим вопросам можете обратиться к администратору @problemaprod .')
    except Exception as e:
        await callback.message.answer('Что то пошло не так')


class Message(StatesGroup):
    user_id = State()
    message = State()


@shop_router.callback_query(F.data.startswith('shipmessage_'), StateFilter(None))
async def write_to_user(callback: types.CallbackQuery, bot: Bot, state: FSMContext, session: AsyncSession):
    if callback.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(Message.user_id)
            order = await orm_check_order_shop(session=session, order_shop_id=int(callback.data.split('_')[-1]))
            await state.update_data(user_id=order.user_id)
            await state.set_state(Message.message)
            await callback.message.answer('Введите ваше сообщение')


@shop_router.message(Message.message, F.text)
async def add_message(message: types.Message, session: AsyncSession, bot: Bot, state: FSMContext):
    await state.update_data(message=message.text)
    data = await state.get_data()
    user = await orm_check_user(user_id=data['user_id'], session=session)
    chat_id = user.chat_id
    try:
        await bot.send_message(chat_id=chat_id,
                               text=f"Администратор отправил вам сообщение:\n\n'{data['message']}'.\n\nДля того чтобы ответить свяжитесь с администратором @problemaprod")
        await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)

        await message.answer('Сообщение отправлено')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer('Что то пошло не так')

# class ShopProduct(StatesGroup):
#     image = State()
#     title = State()
#     price = State()
#     description = State()
#     store_section = State()
#
#
# @shop_router.message(F.text == 'SHOP Добавить товар', StateFilter(None))
# async def add_shop_product(message: types.Message, bot: Bot, state: FSMContext):
#     if message.from_user.id in bot.my_admins_list:
#         current_state = await state.get_state()
#         if current_state is None:
#             await state.set_state(ShopProduct.image)
#             await message.answer('Добавьте фотографию', reply_markup=cancel_kb)
#         else:
#             await message.answer('Действия отменены', reply_markup=admin_start_kb)
#             await state.clear()
#
#
# @shop_router.message(ShopProduct.image, F.text)
# async def check_photo(message: types.Message, state: FSMContext):
#     if message.text:
#         await message.answer('Это не фото, пожалуйста добавьте фото')
#         await state.set_state(ShopProduct.image)
#
#
# @shop_router.message(ShopProduct.image, F.photo)
# async def add_image(message: types.Message, state: FSMContext):
#     image = message.photo[-1].file_id
#     await state.update_data(image=image)
#     await state.set_state(ShopProduct.title)
#     await message.answer('Введите название товара')
#
#
# @shop_router.message(ShopProduct.title, F.text)
# async def add_title(message: types.Message, state: FSMContext):
#     await state.update_data(title=message.text)
#     await state.set_state(ShopProduct.price)
#     await message.answer('Введите цену')
#
#
# @shop_router.message(ShopProduct.price, F.text)
# async def add_price(message: types.Message, state: FSMContext):
#     await state.update_data(price=float(message.text))
#     await state.set_state(ShopProduct.description)
#     await message.answer('Введите описание')
#
#
# @shop_router.message(ShopProduct.description, F.text)
# async def add_description(message: types.Message, state: FSMContext, session: AsyncSession):
#     await state.update_data(description=message.text, store_section='Shop')
#     data = await state.get_data()
#     try:
#         await orm_create_product(session=session, data=data)
#         await message.answer('Продукт добавлен')
#         await state.clear()
#     except Exception as e:
#         await state.clear()
#         await message.answer('Что то пошло не так')
