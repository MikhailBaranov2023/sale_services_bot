from aiogram import Router, types, Bot, F
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.database.orm_query.orm_order import orm_get_services_order_wait_complete, \
    orm_get_all_orders_awaiting_calculate, orm_get_all_orders_waiting_for_payment, orm_get_cancel_orders
from src_bot.database.orm_query.orm_order_shop import orm_get_all_shop_orders_awaiting_calculate, \
    orm_get_all_shop_orders_waiting_for_payment, orm_get_order_shop_wait_complete, orm_get_order_shop_wait_shipping, \
    orm_get_all_cancel_order_shop
from src_bot.database.orm_query.orm_users import orm_check_user

admin_main_menu_roter = Router()

"""orders awaiting calculate"""


@admin_main_menu_roter.message(F.text == 'Заказы ожидающие расчета')
async def get_orders_awaiting_calculate(message: types.Message, bot: Bot, session: AsyncSession):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            """orders"""
            orders = await orm_get_all_orders_awaiting_calculate(session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#{order.type}\nCервис для оплаты -{order.url},\nОписание - {order.description},\nПользователь удален,\nЗаказ не оплачен.",
                        reply_markup=get_callback_btns(btns={
                            'Расчитать': f'calculate_{order.id}',
                            'Отменить': f'cancel_{order.id}',
                            'Написать клиенту': f'message_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#{order.type}\nCервис для оплаты -{order.url},\nОписание - {order.description}\nПользователь - @{user.user_name},\nЗаказ не оплачен.",
                        reply_markup=get_callback_btns(btns={
                            'Расчитать': f'calculate_{order.id}',
                            'Отменить': f'cancel_{order.id}',
                            'Написать клиенту': f'message_{order.id}',
                        }))
                count += 1
                """shop orders"""
            shop_orders = await orm_get_all_shop_orders_awaiting_calculate(session)
            for order in shop_orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#shipping\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ не оплачен.",
                        reply_markup=get_callback_btns(btns={
                            'Расчитать': f'shipcalculate_{order.id}',
                            'Отменить': f'shipcancel_{order.id}',
                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                else:

                    await message.answer(
                        text=f"#shipping\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ не оплачен.",
                        reply_markup=get_callback_btns(btns={
                            'Расчитать': f'shipcalculate_{order.id}',
                            'Отменить': f'shipcancel_{order.id}',
                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                count += 1

            if count == 0:
                await message.answer(
                    text="Нет заказов ожидающих расчета")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


"""orders awaiting payment"""


@admin_main_menu_roter.message(F.text == 'Заказы ожидающие оплаты')
async def get_orders_awaiting_payment(message: types.Message, bot: Bot, session: AsyncSession):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            """orders"""
            orders = await orm_get_all_orders_waiting_for_payment(session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#{order.type}\nCервис для оплаты -{order.url},\nОписание - {order.description},\nПользователь удален,\nЗаказ не оплачен.\nСумма к оплате - {round(order.amount, 0)} руб.",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'paid_{order.id}',
                            'Отменить': f'cancel_{order.id}',
                            'Написать клиенту': f'message_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#{order.type}\nCервис для оплаты -{order.url},\nОписание - {order.description}\nПользователь - @{user.user_name},\nЗаказ не оплачен.\nСумма к оплате - {round(order.amount, 0)} руб.",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'paid_{order.id}',
                            'Отменить': f'cancel_{order.id}',
                            'Написать клиенту': f'message_{order.id}',
                        }))
                count += 1
            """shop orders"""
            shop_orders = await orm_get_all_shop_orders_waiting_for_payment(session)
            for order in shop_orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#shipping\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ не оплачен.\nСумма к оплате - {round(order.amount, 0)} руб.",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'shippaid_{order.id}',
                            'Отменить': f'shipcancel_{order.id}',
                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#shipping\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ не оплачен.\nСумма к оплате - {round(order.amount, 0)} руб.",
                        reply_markup=get_callback_btns(btns={
                            'Оплачено': f'shippaid_{order.id}',
                            'Отменить': f'shipcancel_{order.id}',
                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                count += 1

            if count == 0:
                await message.answer(
                    text="Нет заказов ожидающих оплаты")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


"""orders await complete"""


@admin_main_menu_roter.message(F.text == 'Заказы ожидающие исполнения')
async def get_order_awaiting_complete(message: types.Message, bot: Bot, session: AsyncSession):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_services_order_wait_complete(session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#{order.type}\nCервис для оплаты -{order.url},\nОписание - {order.description},\nПользователь удален,\nЗаказ оплачен.\nСумма к оплате - {round(order.amount, 0)} руб.",
                        reply_markup=get_callback_btns(btns={
                            'Исполнено': f'complete_{order.id}',
                            'Отменить': f'cancel_{order.id}',
                            'Написать клиенту': f'message_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#{order.type}\nCервис для оплаты -{order.url},\nОписание - {order.description}\nПользователь - @{user.user_name},\nЗаказ оплачен.\nСумма к оплате - {round(order.amount, 0)} руб.",
                        reply_markup=get_callback_btns(btns={
                            'Исполнено': f'complete_{order.id}',
                            'Отменить': f'cancel_{order.id}',
                            'Написать клиенту': f'message_{order.id}',
                        }))
                count += 1
            orders_shop = await orm_get_order_shop_wait_shipping(session)
            for order in orders_shop:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#shipping\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ ожидает доставки.\nСумма к оплате - {round(order.amount, 0)} руб.",
                        reply_markup=get_callback_btns(btns={
                            'Отправлен': f'sent_{order.id}',
                            'Отменить': f'shipcancel_{order.id}',
                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#shipping\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ ожидает доставки.\nСумма к оплате - {round(order.amount, 0)} руб.\nТелефон - {user.phone}",
                        reply_markup=get_callback_btns(btns={
                            'Отправлен': f'sent_{order.id}',
                            'Отменить': f'shipcancel_{order.id}',
                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет заказов ожидающих исполнения ")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@admin_main_menu_roter.message(F.text == 'Заказы в доставке')
async def get_orders_in_delivery(message: types.Message, bot: Bot, session: AsyncSession):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            shop_order = await orm_get_order_shop_wait_complete(session)
            for order in shop_order:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#shipping\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nЗаказ в доставке.\nСумма к оплате - {round(order.amount, 0)} руб.\nТрек-номер - {order.track_number}",
                        reply_markup=get_callback_btns(btns={
                            'Доставлен': f'shipcomplete_{order.id}',
                            'Отменить': f'shipcancel_{order.id}',
                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                else:
                    await message.answer(
                        text=f"#shipping\nТовары -{order.url},\nОписание - {order.description}\nПользователь - @{user.user_name},\nЗаказ в доставке.\nСумма к оплате - {round(order.amount, 0)} руб.\nТрек-номер - {order.track_number}",
                        reply_markup=get_callback_btns(btns={
                            'Доставлен': f'shipcomplete_{order.id}',
                            'Отменить': f'shipcancel_{order.id}',
                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет заказов ожидающих доставки ")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@admin_main_menu_roter.message(F.text == 'Отмененные заказы')
async def get_all_canceled_order(message: types.Message, bot: Bot, session: AsyncSession):
    count = 0
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_cancel_orders(session=session)
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#{order.type}\nЗаказ отменен.\nCервис для оплаты -{order.url},\nОписание - {order.description},\nПользователь удален,\n")
                else:
                    await message.answer(
                        text=f"#{order.type}\nЗаказ отменен.\nCервис для оплаты -{order.url},\nОписание - {order.description},\nПользователь - @{user.user_name}",
                        reply_markup=get_callback_btns(btns={
                            'Написать клиенту': f'message_{order.id}',
                        }))
                count += 1

            shop_orders = await orm_get_all_cancel_order_shop(session=session)
            for order in shop_orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#shipping\nЗаказ отменен.\nТовары - {order.url},\n,\nОписание - {order.description},\nПользователь удален.")
                else:
                    await message.answer(
                        text=f"#shipping\nЗаказ отменен.\nТовары -{order.url},\nОписание - {order.description}\nПользователь - @{user.user_name}",
                        reply_markup=get_callback_btns(btns={

                            'Написать клиенту': f'shipmessage_{order.id}',
                        }))
                count += 1
            if count == 0:
                await message.answer(
                    text="Нет отменных заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')

    else:
        await message.answer(message.text)