from sqlalchemy.ext.asyncio import AsyncSession






async def get_menu_content(
        session: AsyncSession,
        level: int,
        menu_name: str
):
    if level == 0:
        return await store_menu(session, menu_name, level)
