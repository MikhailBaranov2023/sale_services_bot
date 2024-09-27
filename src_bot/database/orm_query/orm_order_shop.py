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


async def orm_get_order_shop(session: AsyncSession, data: dict):
    query = select(OrderShop).where(OrderShop.url == data['url'],
                                    OrderShop.description == data['description'],
                                    OrderShop.address == data['address'],
                                    OrderShop.user_id == data['user_id'], )
    result = await session.execute(query)
    return result.scalar()


async def orm_get_all_shop_orders_awaiting_calculate(session: AsyncSession):
    query = select(OrderShop).where(OrderShop.payment_status == False, OrderShop.cancel_status == False,
                                    OrderShop.amount == None)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_all_shop_orders_waiting_for_payment(session: AsyncSession):
    query = select(OrderShop).where(OrderShop.payment_status == False, OrderShop.cancel_status == False,
                                    OrderShop.amount != None)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_all_cancel_order_shop(session: AsyncSession):
    query = select(OrderShop).where(OrderShop.cancel_status == True)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_all_complete_order_shop(session: AsyncSession):
    query = select(OrderShop).where(OrderShop.order_status == True)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_update_order_shop_amount(session: AsyncSession, amount, order_shop_id: int):
    query = update(OrderShop).where(OrderShop.id == order_shop_id).values(
        amount=float(amount),
    )
    await session.execute(query)
    await session.commit()


async def orm_order_shop_update_payment_status(session: AsyncSession, order_shop_id: int):
    query = update(OrderShop).where(OrderShop.id == order_shop_id).values(
        payment_status=True
    )
    await session.execute(query)
    await session.commit()


async def orm_add_track_code(session: AsyncSession, track_number, order_shop_id: int):
    query = select(OrderShop).where(OrderShop.id == order_shop_id)
    result = await session.execute(query)
    obj = result.scalar()
    if obj.track_number == None:
        query = update(OrderShop).where(OrderShop.id == order_shop_id).values(
            track_number=track_number,
        )
        await session.execute(query)
        await session.commit()
        return True
    else:
        return False


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
    query = select(OrderShop).order_by(OrderShop.created).where(OrderShop.user_id == user_id,
                                                                OrderShop.cancel_status == False)
    result = await session.execute(query)
    return result.scalars()


async def orm_get_order_shop_wait_shipping(session: AsyncSession):
    query = select(OrderShop).where(OrderShop.payment_status == True, OrderShop.track_number == None,
                                    OrderShop.order_status == False, OrderShop.cancel_status == False)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_order_shop_wait_complete(session: AsyncSession):
    query = select(OrderShop).where(OrderShop.order_status == False, OrderShop.track_number != None,
                                    OrderShop.payment_status == True, OrderShop.cancel_status == False)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_complete_order_shop(session: AsyncSession, order_shop_id: int):
    query = update(OrderShop).where(OrderShop.id == order_shop_id).values(
        order_status=True
    )
    await session.execute(query)
    await session.commit()
