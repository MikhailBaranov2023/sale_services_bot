from sqlalchemy.ext.asyncio import AsyncSession
from src_bot.database.models import Product
from sqlalchemy import select, update, delete


async def orm_create_product(session: AsyncSession, data: dict):
    obj = Product(
        title=data['title'],
        image=data['image'],
        price=data['price'],
        store_section=data['store_section'],
        description=data['description'],
    )
    session.add(obj)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()


async def orm_get_product_shop(session: AsyncSession):
    query = select(Product).where(Product.store_section == 'Shop')
    result = await session.execute(query)
    return result.scalar()


async def orm_get_product_services(session: AsyncSession):
    query = select(Product).where(Product.store_section == 'Services')
    result = await session.execute(query)
    return result.scalar()


async def orm_get_product_ps(session: AsyncSession):
    query = select(Product).where(Product.store_section == 'PS Store')
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, id: int):
    query = select(Product).where(Product.id == id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_product_ps_subs(session: AsyncSession, name):
    query = select(Product).where(Product.store_section == 'PS Store', Product.title.ilike(f'%{name}%')).order_by(
        Product.price)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_update_product(session: AsyncSession, product_id: int, data: dict):
    query = update(Product).where(Product.id == product_id).values(
        title=data['title'],
        image=data['image'],
        price=data['price'],
        description=data['description'],
    )
    await session.execute(query)
    await session.commit()


async def orm_update_description_to_shop(session: AsyncSession, description: str):
    query = update(Product).where(Product.store_section == 'Shop').values(
        description=description,
    )
    await session.execute(query)
    await session.commit()


async def orm_update_image_to_shop(session: AsyncSession, image: str):
    query = update(Product).where(Product.store_section == 'Shop').values(
        image=image,
    )
    await session.execute(query)
    await session.commit()


async def orm_update_image_to_services(session: AsyncSession, image: str):
    query = update(Product).where(Product.store_section == 'Services').values(
        image=image,
    )
    await session.execute(query)
    await session.commit()


async def orm_update_image_to_ps(session: AsyncSession, image: str):
    query = update(Product).where(Product.store_section == 'PS Store').values(
        image=image,
    )
    await session.execute(query)
    await session.commit()


async def get_product_to_title(session: AsyncSession, title: str):
    query = select(Product).where(Product.title == title)
    result = await session.execute(query)
    return result.scalar()
