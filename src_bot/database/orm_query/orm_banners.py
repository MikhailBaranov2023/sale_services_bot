from sqlalchemy.ext.asyncio import AsyncSession
from src_bot.database.models import Banner
from sqlalchemy import select, update, delete


async def orm_add_banner_ps(session: AsyncSession, data: dict):
    obj = Banner(
        image=data['image'],
        description=data['description'],
        type='PS Store',
    )
    session.add(obj)
    await session.commit()


async def orm_add_banner(session: AsyncSession, data: dict):
    obj = Banner(
        image=data['image'],
        description=data['description'],
        type=data['type']
    )
    session.add(obj)
    await session.commit()


async def orm_get_banner_ps(session: AsyncSession, type):
    query = select(Banner).where(Banner.type == type)
    result = await session.execute(query)
    return result.scalar()
