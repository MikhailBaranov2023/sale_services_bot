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


async def orm_create_order_games(session: AsyncSession, data: dict):
    obj = Order(
        type=data['type'],
        description=data['description'],
        user_id=data['user_id'],
        url=data['url'],
        amount=data['price']
    )
    session.add(obj)
    await session.commit()


async def orm_create_order_game(session: AsyncSession, data: dict):
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
    query = select(Order).where(Order.user_id == user_id, Order.cancel_status == False)
    result = await session.execute(query)
    return result.scalars()


async def orm_get_all_orders_awaiting_calculate(session: AsyncSession):
    query = select(Order).order_by(Order.created).where(Order.payment_status == False,
                                                        Order.cancel_status == False, Order.amount == None)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_all_orders_waiting_for_payment(session: AsyncSession):
    query = select(Order).order_by(Order.created).where(Order.payment_status == False,
                                                        Order.cancel_status == False, Order.amount != None)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_update_amount_order(session: AsyncSession, amount, order_id: int):
    query = update(Order).where(Order.id == order_id).values(
        amount=float(amount)
    )
    await session.execute(query)
    await session.commit()


async def orm_get_cancel_orders(session: AsyncSession):
    query = select(Order).where(Order.cancel_status == True)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_services_order_wait_complete(session: AsyncSession):
    query = select(Order).order_by(Order.created).where(Order.order_status == False, Order.payment_status == True,
                                                        Order.cancel_status == False)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_complete_order(session: AsyncSession, order_id: int):
    query = update(Order).where(Order.id == order_id).values(
        order_status=True
    )
    await session.execute(query)
    await session.commit()


async def orm_get_completed_order(session: AsyncSession):
    query = select(Order).where(Order.order_status == False)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_order_update_payment_status(session: AsyncSession, order_id: int):
    query = update(Order).where(Order.id == order_id).values(
        payment_status=True
    )
    await session.execute(query)
    await session.commit()
