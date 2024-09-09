import os

from dotenv import load_dotenv, find_dotenv
import asyncio

from aiogram import Bot, Dispatcher, types

from src_bot.bot.handlers.user_private_handlers.user_private_handler import user_private_router
from src_bot.bot.handlers.admin_private_handlers.admin_private_handler import admin_private_router
from src_bot.middlewares.db import DataBaseSession

load_dotenv(find_dotenv())

from src_bot.database.engine import create_db, drop_db, session_maker

from src_bot.bot.commands.commands_list import commands

# ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']
bot = Bot(token=os.getenv("TG_TOKEN"))
bot.my_admins_list = [361467867]

dp = Dispatcher()
dp.include_routers(user_private_router, admin_private_router, )


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()
    print('Бот вышел  в онлайн')


async def on_shutdown(bot):
    print('Бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.set_my_commands(commands=commands, scope=types.BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
