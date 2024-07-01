from aiogram.filters import CommandStart, StateFilter
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from src_bot.bot.keyboards.main_menu import user_start_kb
from src_bot.bot.keyboards.games_keyboards import games_kbd

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start(message: types.Message, bot: Bot):
    if message.from_user.id in bot.my_admins_list:
        await message.answer('Вы в админке')
    else:
        await message.answer('Я Работаю', reply_markup=user_start_kb)


@user_private_router.message(F.text == "Назад")
async def games_keyboard(message: types.Message):
    await message.answer('Главное меню', reply_markup=user_start_kb)


class Services(StatesGroup):
    url = State()
    description = State()
    username = State()


@user_private_router.message(F.text == 'Оплата сервисов', StateFilter(None))
async def pay_services(message: types.Message, state: FSMContext):
    await message.answer('Введите ссылку на сервис который хотите оплатить')
    await state.set_state(Services.url)


@user_private_router.message(Services.url, F.text)
async def add_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer('Введите описание')
    await state.set_state(Services.description)


@user_private_router.message(Services.description, F.text)
async def add_description(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(description=message.text, username=message.from_user.username)
    data = await state.get_data()
    await message.answer(f'{data["url"]},{data["description"]}')
    print(bot.my_admins_list[0])
    await bot.send_message(chat_id=bot.my_admins_list[0],
                           text=f'НОВАЯ ЗАЯВКА\nсервис - {data["url"]},\nописание - {data["description"]},\nпользователь - @{data["username"]}')
    await state.clear()


@user_private_router.message(F.text == "Игровые платформы")
async def games_keyboard(message: types.Message):
    await message.answer(text=message.text, reply_markup=games_kbd)
