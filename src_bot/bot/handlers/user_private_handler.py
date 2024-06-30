from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types, Router

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Я Работаю')
