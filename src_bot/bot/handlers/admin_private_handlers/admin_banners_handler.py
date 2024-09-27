from aiogram import Bot, Dispatcher, types, Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src_bot.bot.keyboards.main_menu import admin_short_kb
from src_bot.database.orm_query.orm_banners import orm_add_banner

banner_router = Router()


class Banner(StatesGroup):
    image = State()
    type = State()
    description = State()


@banner_router.message(F.text == "Добавить баннер")
async def add_banner(message: types.Message, session: AsyncSession, bot: Bot, state: FSMContext):
    if message.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(Banner.image)
            await message.answer('Добавьте фотографию')
    else:
        await message.answer('Действия отменены', reply_markup=admin_short_kb)
        await state.clear()


@banner_router.message(Banner.image, F.text)
async def check_photo_banner(message: types.Message, state: FSMContext):
    if message.text:
        await message.answer('Это не фото, пожалуйста добавьте фото')
        await state.set_state(Banner.image)


@banner_router.message(Banner.image, F.photo)
async def add_photo_banner(message: types.Message, state: FSMContext):
    image = message.photo[-1].file_id
    await state.update_data(image=image)
    await state.set_state(Banner.type)
    await message.answer('Введите тип')


@banner_router.message(Banner.type, F.text)
async def add_banner_type(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)
    await state.set_state(Banner.description)
    await message.answer('Введите описание')


@banner_router.message(Banner.description, F.text)
async def add_description_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.text)
    data = await state.get_data()
    try:
        await orm_add_banner(session=session, data=data)
        await message.answer('Баннер добавлен')
        await state.clear()
    except Exception as e:
        await message.answer('Что то пошло не так')
        await state.clear()


