from sqlalchemy.ext.asyncio import AsyncSession
from src_bot.database.models import User
from sqlalchemy import select, update, delete


async def orm_add_user(session: AsyncSession, chat_id: int, user_name: str, ):
    obj = User(
        chat_id=chat_id,
        user_name=user_name,
    )
    session.add(obj)
    await session.commit()


async def orm_check_user(session: AsyncSession, chat_id: int):
    query = select(User).where(User.chat_id == chat_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalar()
