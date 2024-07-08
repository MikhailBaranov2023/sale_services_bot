from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.database.orm_query import orm_get_orders_shop

admin_private_router = Router()


@admin_private_router.message(F.text == 'все заказы')
async def all_shop_orders(message: types.Message, session: AsyncSession, bot):
    if message.from_user.id in bot.my_admins_list:
        orders = await orm_get_orders_shop(session)
        for order in orders:
            await message.answer(
                text=f"#SHOP\nтовары-{order.product_urls},\nадрес доставки-{order.address},\nописание - {order.description},\nстатус оплаты{order.payment_status},\nстатус заказа-{order.order_status}")
    else:
        await message.answer('У вас нет прав')
