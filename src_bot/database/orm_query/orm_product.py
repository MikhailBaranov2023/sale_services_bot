from sqlalchemy.ext.asyncio import AsyncSession
from src_bot.database.models import Product
from sqlalchemy import select, update, delete


async def orm_create_product(session: AsyncSession, date: dict):
    obj = Product(
        title=date['title'],
        image=date['image'],
        price=date['price'],
        description=date['description'],
    )
    session.add(obj)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()


