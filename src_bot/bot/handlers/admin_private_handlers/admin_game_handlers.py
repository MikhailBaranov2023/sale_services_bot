from aiogram import Bot, Dispatcher, types, Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.main_menu import admin_short_kb
from src_bot.database.orm_query.orm_product import orm_create_product, orm_update_product, orm_get_product_ps

games_router = Router()


class GAMEProduct(StatesGroup):
    image = State()
    title = State()
    price = State()
    store_section = State()
    description = State()


@games_router.message(F.text == 'GAME Добавить товар')
async def add_games_product(message: types.Message, bot: Bot, state: FSMContext):
    if message.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(GAMEProduct.image)
            await message.answer('Добавьте фотографию')
        else:
            await message.answer('Действия отменены', reply_markup=admin_short_kb)
            await state.clear()


@games_router.message(GAMEProduct.image, F.text)
async def check_photo_games(message: types.Message, state: FSMContext):
    if message.text:
        await message.answer('Это не фото, пожалуйста добавьте фото')
        await state.set_state(GAMEProduct.image)


@games_router.message(GAMEProduct.image, F.photo)
async def add_image_games(message: types.Message, state: FSMContext):
    image = message.photo[-1].file_id
    await state.update_data(image=image)
    await state.set_state(GAMEProduct.title)
    await message.answer('Введите название товара')


@games_router.message(GAMEProduct.title, F.text)
async def add_title_games(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(GAMEProduct.price)
    await message.answer('Введите цену')


@games_router.message(GAMEProduct.price, F.text)
async def add_price_games(message: types.Message, state: FSMContext):
    await state.update_data(price=float(message.text))
    await state.set_state(GAMEProduct.store_section)
    await message.answer('Введите название раздела в формате:\n"PS Store", "MS Store", "Steam"')


@games_router.message(GAMEProduct.store_section, F.text)
async def add_store_section_games(message: types.Message, state: FSMContext):
    await state.update_data(store_section=message.text)
    await state.set_state(GAMEProduct.description)
    await message.answer('Введите описание')


@games_router.message(GAMEProduct.description, F.text)
async def add_description_services(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.text)
    data = await state.get_data()
    try:
        await orm_create_product(session=session, data=data)
        await state.clear()
        await message.answer('Продукт добавлен')
    except Exception as e:
        await state.clear()
        await message.answer('Что то пошло не так')


@games_router.message(F.text == 'GAME Изменить товар')
async def change_games_product(message: types.Message, session: AsyncSession):
    data = await orm_get_product_ps(session=session)
    for product in data:
        await message.answer_photo(photo=product.image,
                                   caption=f"{product.title}\n\nЦена - {round(product.price, 2)}руб\n\n{product.description}",
                                   reply_markup=get_callback_btns(btns={
                                       'Изменить': f'GAMEupdate_{product.id}',
                                       'Удалить': f'GAMEdelete_{product.id}'
                                   }))


class ProductUpdate(StatesGroup):
    image = State()
    title = State()
    price = State()
    product_id = State()
    description = State()


@games_router.callback_query(F.data.startswith('GAMEupdate_'))
async def update_ps_store(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.from_user.id in bot.my_admins_list:
        current_state = await state.get_state()
        if current_state is None:
            await state.set_state(ProductUpdate.product_id)
            await state.update_data(product_id=int(callback.data.split('_')[-1]))
            await state.set_state(ProductUpdate.image)
            await callback.message.answer('Добавьте фотографию')
        else:
            await callback.message.answer('Действия отменены', reply_markup=admin_short_kb)
            await state.clear()


@games_router.message(ProductUpdate.image, F.text)
async def check_photo_games(message: types.Message, state: FSMContext):
    if message.text:
        await message.answer('Это не фото, пожалуйста добавьте фото')
        await state.set_state(ProductUpdate.image)


@games_router.message(ProductUpdate.image, F.photo)
async def add_image_games(message: types.Message, state: FSMContext):
    image = message.photo[-1].file_id
    print(image)
    await state.update_data(image=image)
    await state.set_state(ProductUpdate.title)
    await message.answer('Введите название товара')


@games_router.message(ProductUpdate.title, F.text)
async def add_title_games(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(ProductUpdate.price)
    await message.answer('Введите цену')


@games_router.message(ProductUpdate.price, F.text)
async def add_price_games(message: types.Message, state: FSMContext):
    await state.update_data(price=float(message.text))
    await state.set_state(ProductUpdate.description)
    await message.answer('Введите описание')


@games_router.message(ProductUpdate.description, F.text)
async def add_description_services(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.text, store_section=None)
    data = await state.get_data()
    try:
        await orm_update_product(session=session, data=data, product_id=data['product_id'])
        await state.clear()
        await message.answer('Продукт изменен')
    except Exception as e:
        await state.clear()
        await message.answer('Что то пошло не так')
