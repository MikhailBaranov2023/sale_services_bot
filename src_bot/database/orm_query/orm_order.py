from sqlalchemy.ext.asyncio import AsyncSession
from src_bot.database.models import Order
from sqlalchemy import select, update, delete


async def orm_create_order(session: AsyncSession, data: dict):
    obj = Order(
        type=data['type'],
        description=data['description'],
        user_id=data['user_id'],
        url=data['url'],
    )
    session.add(obj)
    await session.commit()


async def orm_get_order(session: AsyncSession, data: dict):
    query = select(Order).where(Order.type == data['type'],
                                Order.description == data['description'],
                                Order.user_id == data['user_id'],
                                Order.url == data['url'])
    result = await session.execute(query)
    return result.scalar()


async def orm_update_order(session: AsyncSession, amount, order_id: int):
    query = update(Order).where(Order.id == order_id).values(
        amount=float(amount),
        payment_status=True,
    )
    await session.execute(query)
    await session.commit()


async def orm_cancel_order(session: AsyncSession, order_id: int):
    query = update(Order).where(Order.id == order_id).values(
        cancel_status=True
    )
    await session.execute(query)
    await session.commit()


async def orm_check_order(session: AsyncSession, order_id: int):
    query = select(Order).where(Order.id == order_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_user_orders(session: AsyncSession, user_id: int):
    query = select(Order).where(Order.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()
