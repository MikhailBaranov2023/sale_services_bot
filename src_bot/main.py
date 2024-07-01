import os
import asyncio

from aiogram import Bot, Dispatcher, types

from settings import TG_TOKEN
from src_bot.bot.handlers.user_private_handler import user_private_router
from src_bot.bot.handlers.admin_private_handler import admin_private_router

ALLOWED_UPDATES = ['message', 'edited_message', ]
bot = Bot(TG_TOKEN)
bot.my_admins_list = [361467867]

dp = Dispatcher()
dp.include_routers(user_private_router,admin_private_router)


async def main():
    print('Бот вышел  в онлайн')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
