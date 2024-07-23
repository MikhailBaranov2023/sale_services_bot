from sqlalchemy.ext.asyncio import AsyncSession
from src_bot.database.models import OrderShop
from sqlalchemy import select, update, delete


async def orm_create_order_shop(session: AsyncSession, data: dict):
    obj = OrderShop(
        url=data['url'],
        description=data['description'],
        address=data['address'],
        user_id=data['user_id'],
    )
    session.add(obj)
    await session.commit()


async def orm_update_order_shop(session: AsyncSession, amount, order_shop_id: int):
    query = update(OrderShop).where(OrderShop.id == order_shop_id).values(
        amount=float(amount),
        payment_status=True,
    )
    await session.execute(query)
    await session.commit()


async def orm_add_track_code(session: AsyncSession, track_number, order_shop_id: int):
    query = update(OrderShop).where(OrderShop.id == order_shop_id).values(
        track_number=track_number,
    )
    await session.execute(query)
    await session.commit()


async def orm_update_status(session: AsyncSession, order_shop_id: int):
    query = update(OrderShop).where(OrderShop.id == order_shop_id).values(
        order_status=True
    )
    await session.execute(query)
    await session.commit()


async def orm_cancel_order_shop(session: AsyncSession, order_shop_id: int):
    query = update(OrderShop).where(OrderShop.id == order_shop_id).values(
        cancel_status=True
    )
    await session.execute(query)
    await session.commit()


async def orm_check_order_shop(session: AsyncSession, order_shop_id: int):
    query = select(OrderShop).where(OrderShop.id == order_shop_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_user_shop_orders(session: AsyncSession, user_id: int):
    query = select(OrderShop).where(OrderShop.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()
