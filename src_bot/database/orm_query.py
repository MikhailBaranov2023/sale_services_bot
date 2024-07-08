from sqlalchemy.ext.asyncio import AsyncSession
from src_bot.database.models import OrderShop, Order, Product, User
from sqlalchemy import select, update, delete


async def orm_create_order_shop(session: AsyncSession, data: dict):
    """create order shop"""
    obj = OrderShop(
        product_urls=data['url'],
        address=data['address'],
        description=data['description'],
    )
    session.add(obj)
    await session.commit()


async def orm_get_orders_shop(session: AsyncSession):
    """get all orders shop"""
    query = select(OrderShop)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_order_shop(session: AsyncSession, data):
    query = select(OrderShop).where(OrderShop.product_urls == data['url'])
    result = await session.execute(query)
    return result.scalars()
