from aiogram import F, types, Bot, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src_bot.bot.keyboards.inline import get_callback_btns
from src_bot.bot.keyboards.main_menu import cancel_kb, user_start_kb
from src_bot.bot.keyboards.profile_kbd import register_kbd
from src_bot.database.orm_query.orm_order_shop import orm_create_order_shop, orm_get_order_shop
from src_bot.database.orm_query.orm_users import orm_check_user_chat_id

user_shop_order = Router()


class OrderShop(StatesGroup):
    url = State()
    address = State()
    description = State()
    user_id = State()
    user_name = State()


@user_shop_order.callback_query(F.data == 'make_order', StateFilter(None))
async def shop_make_order(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is None:
        if await orm_check_user_chat_id(session, chat_id=callback.from_user.id) is not None:
            await callback.message.answer(
                'Введите ссылку на товар\товары.\nТовары могут быть с разных платформ в неограниченном количестве.\n В случае если товаров несколько введите несолько ссылок в формате\n "https://www.adidas.pt/sapatilhas-campus-00s/HQ8707.html?forceSelSize=HQ8707_620\n\nhttps://www.adidas.pt/sapatilhas-ny-90/JI1893.html?pr=cart_rr&slot=4&rec=mt"',
                reply_markup=cancel_kb)
            await state.set_state(OrderShop.url)
        else:
            await callback.message.answer('Для того чтобы продолжить вам необходимо зарегистрироваться.',
                                          reply_markup=register_kbd)
            await state.clear()
    else:
        await state.clear()
        await callback.message.answer('Формирования заявки отменено.', reply_markup=user_start_kb)


@user_shop_order.message(OrderShop.url, F.text)
async def add_url_order(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(
        'Введите адрес.\nВведенный вами адрес будет указан при отправке товара, пожалуйста убедитесь что вы ввели адрес в формате:\nРоссия, Москва, Тверская улица, д.2, кв.1, 109012')
    await state.set_state(OrderShop.address)


@user_shop_order.message(OrderShop.address, F.text)
async def add_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(
        'Введите описание.\n\nЗдесь вы можете указать дополнительную информацию необходимую для оплаты,\n\n Например, это может быты размер, желаемый цвет, промокод и тд.\n\nПомимо этого, вы можете написать сюда дополнительные вопросы связанные с конкретным заказом которые хотели бы задать администратору')
    await state.set_state(OrderShop.description)


@user_shop_order.message(OrderShop.description, F.text)
async def add_description_order(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user = await orm_check_user_chat_id(session, chat_id=message.from_user.id)
    await state.update_data(description=message.text, user_id=user.id)
    data = await state.get_data()
    try:
        await orm_create_order_shop(session, data)
        await message.answer(
            'Ваша заявка принята.\n\nВ ближайшее время мы рассчитаем итоговую стоимость и пришлем вам реквизиты для оплаты.',
            reply_markup=user_start_kb)
        order = await orm_get_order_shop(session, data)
        await bot.send_message(chat_id=bot.my_admins_list[0],
                               text=f"#shipping\nТовары - {order.url},\nАдрес доставки - {order.address},\nОписание - {order.description},\nПользователь - @{user.user_name},\nЗаказ не оплачен.",
                               reply_markup=get_callback_btns(btns={
                                   'Расчитать': f'shipcalculate_{order.id}',
                                   'Отменить': f'shipcancel_{order.id}',
                                   'Написать клиенту': f'shipmessage_{order.id}',
                               }))

        await state.clear()
    except Exception as e:
        await message.answer('Что пошло не так. Пожалуйста свяжитесь с aдминистратором или попробуйте позже.',
                             reply_markup=user_start_kb)
        await state.clear()
