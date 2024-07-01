from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart

admin_private_router = Router()


@admin_private_router.message(CommandStart())
async def admin_start(message: types.Message, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await message.answer('Вы в админке')
