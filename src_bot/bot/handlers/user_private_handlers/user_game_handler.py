from aiogram import Router, types, Bot, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.handlers.menu_processing import get_menu_content
from src_bot.bot.keyboards.inline import MenuCallBack
from src_bot.bot.keyboards.main_menu import user_start_kb

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.profile_kbd import register_kbd
from src_bot.database.orm_query.orm_order import orm_create_order_games, orm_get_order, orm_create_order_game
from src_bot.database.orm_query.orm_product import orm_get_product
from src_bot.database.orm_query.orm_users import orm_check_user_chat_id

user_game_router = Router()


@user_game_router.message(F.text == 'PS Store')
async def ps_store(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name="PS Store")
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


@user_game_router.callback_query(MenuCallBack.filter())
async def ps_store_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=callback_data.level, menu_name=callback_data.menu_name,
                                                 product_id=callback_data.product)

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


class PSGame(StatesGroup):
    url = State()
    type = State()
    user_id = State()
    description = State()


@user_game_router.callback_query(F.data == 'ps_game')
async def by_ps_game(callback: types.CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        user = await orm_check_user_chat_id(session, chat_id=callback.from_user.id)
        if user is not None:
            await state.update_data(type='games', user_id=user.id)
            await state.set_state(PSGame.url)
            await callback.message.answer('Пожалуйста введите ссылку на игру или название')
        else:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await callback.message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                          reply_markup=register_kbd)
            await state.clear()
    else:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await callback.message.answer('Действия отменены', reply_markup=user_start_kb)
        await state.clear()


@user_game_router.message(PSGame.url, F.text)
async def add_game(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(PSGame.description)
    await message.answer(
        'Введите данные для входа в аккаунт. Ваш аккаунт должен быть зарегистрирован в регионе Индия.\n\n Если у вас нет аккаунта, мы можем создать его для вас. Это будет стоить дополнительно 200 рублей.\n\nДля того чтобы создать аккаунт ответьте на это сообщение "Создать аккаунт"\n\nЕсли хотите отменить действие напишите отменить.',
        reply_markup=get_callback_btns(btns={'Отменить': 'cancel', }))


@user_game_router.message(PSGame.description, F.text)
async def add_description_game(message: types.Message, session: AsyncSession, bot: Bot, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    # try:
    user = await orm_check_user_chat_id(session, chat_id=message.from_user.id)
    await orm_create_order_game(session=session, data=data)
    order = await orm_get_order(session, data)
    await message.answer(
            f'Ваша заявка принята.\n\nВ ближайшее время c вами свяжется администратор.')
    await state.clear()
    await bot.send_message(chat_id=bot.my_admins_list[0],
                               text=f'#{order.type.upper()}\nИгра - ,\nАккаунт - {order.description},\nПользователь - @{user.user_name}\n', reply_markup=get_callback_btns(btns={
                                   'Расчитать': f'calculate_{order.id}',
                                   'Отменить': f'cancel_{order.id}',
                                   'Написать клиенту': f'message_{order.id}',
                               }))
    # except Exception as e:
    #     await message.answer('Что то пошло не так')


class PSSubscription(StatesGroup):
    url = State()
    price = State()
    type = State()
    user_id = State()
    description = State()


@user_game_router.callback_query(F.data.startswith('psbuy_'))
async def ps_store(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state is None:

        if not await orm_check_user_chat_id(session, chat_id=callback.from_user.id) is None:
            product_id = int(callback.data.split('_')[-1])
            product = await orm_get_product(session=session, id=product_id)

            await state.update_data(url=product.title, price=product.price, type='games')
            await state.set_state(PSSubscription.description)
            await callback.message.answer(
                'Введите данные для входа в аккаунт.\n\n Если у вас нет аккаунта, мы можем создать его для вас. Это будет стоить дополнительно 200 рублей.\n\nДля того чтобы создать аккаунт ответьте на это сообщение "Создать аккаунт"\n\nЕсли хотите отменить действие напишите отменить.',
                reply_markup=get_callback_btns(btns={'Отменить': 'cancel', }))
        else:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await callback.message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                          reply_markup=register_kbd)
            await state.clear()
    else:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await callback.message.answer('Действия отменены', reply_markup=user_start_kb)
        await state.clear()


@user_game_router.message(PSSubscription.description, F.text)
async def add_account(message: types.Message, session: AsyncSession, state: FSMContext, bot: Bot):
    user = await orm_check_user_chat_id(session, chat_id=message.from_user.id)
    await state.update_data(description=message.text, user_id=user.id)
    data = await state.get_data()
    try:
        await orm_create_order_games(session=session, data=data)
        order = await orm_get_order(session, data)
        await message.answer(
            f'Ваша заявка принята.\n\nВ близжайщее время c вами свяжется администратор.\n\nСумма к оплате - {round(order.amount, 0)}руб\n\nВы можете оплатить через СБП по номеру +79998502717(Райфайзенбанк), либо по номеру карты',
            reply_markup=get_callback_btns(btns={'Оплачено': f'ipaid_{order.id}'}))
        await state.clear()
        await bot.send_message(chat_id=bot.my_admins_list[0],
                               text=f'#{order.type.upper()}\nПодписка - {order.url},\nАккаунт - {order.description},\nПользователь - @{user.user_name}\nСумма к оплате - {round(order.amount, 0)}руб')
    except Exception as e:
        await message.answer('Что то пошло не так')


@user_game_router.message(or_f(F.text == 'Steam', F.text == 'Microsoft Store'))
async def steam_or_ms(message: types.Message, bot):
    await message.answer(
        'Мы работаем над тем, чтобы вы могли быстро и удобно оплачивать этот сревис.\n\n Вы можете оставить заявку в разделе "Оплата сервисов", после чего с вами свяжется наш администратор.\n\n ')
