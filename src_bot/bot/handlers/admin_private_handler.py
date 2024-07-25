from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.shipping_kb import shipping_kbd
from src_bot.database.orm_query.orm_order_shop import orm_get_all_current_order_shop, orm_get_all_cancel_order_shop, \
    orm_get_all_complete_order_shop
from src_bot.database.orm_query.orm_users import orm_check_user, orm_get_users

admin_private_router = Router()


@admin_private_router.message(F.text == 'Доставка')
async def services(message: types.Message, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await message.answer(message.text, reply_markup=shipping_kbd)
    else:
        await message.answer(message.text)


@admin_private_router.message(F.text == 'Текущие заказы в доставке')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_all_current_order_shop(session)
            count = 0
            print(count)
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
                    text="Нет текущих заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@admin_private_router.message(F.text == 'Отмененные заказы в доставке')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_all_cancel_order_shop(session)
            count = 0
            for order in orders:
                user = await orm_check_user(session, order.user_id)
                if user is None:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь удален,\nСтатус оплаты - {order.payment_status},\nТрек-номер - {order.track_number}")
                else:
                    await message.answer(
                        text=f"#SHOP\nТовары-{order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nСтатус оплаты - {order.payment_status},\nТрек-номер - {order.track_number}")
                count += 1
                print(count)
            if count == 0:
                await message.answer(
                    text="Нет отмененных заказов")
        except Exception as e:
            await message.answer('При выполнении запроса возникла ошибка.\nПроверьте бота.')
    else:
        await message.answer(message.text)


@admin_private_router.message(F.text == 'Исполненные заказы в доставке')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        try:
            orders = await orm_get_all_complete_order_shop(session)
            count = 0
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


@admin_private_router.message(F.text == 'users')
async def get_all_users(message: types.Message, session: AsyncSession, bot):
    if message.from_user.id in bot.my_admins_list:
        data = await orm_get_users(session)

        for user in data.all():
            await message.answer(f"{user.user_name}\n{user.chat_id},\n{user.referral_code}")
    else:
        await message.answer('У вас нет прав')
