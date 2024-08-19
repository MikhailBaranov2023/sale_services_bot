from aiogram import Router, types, Bot, F

from src_bot.bot.keyboards.games_keyboards import games_kbd

game_menu_router = Router()


@game_menu_router.message(F.text == "Игровые платформы")
async def games_keyboard(message: types.Message):
    await message.answer(text=message.text, reply_markup=games_kbd)

#
# @game_menu_router.message(F.text == 'PS Store')

