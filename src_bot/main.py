import os
import asyncio
import aiohttp
from settings import TG_TOKEN
from aiogram import Bot, Dispatcher, types

bot = Bot(TG_TOKEN)
bot.my_admins_list = [361467867]

dp = Dispatcher()


async def main():
    print('Бот вышел  в онлайн')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
