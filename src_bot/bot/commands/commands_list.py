from aiogram.types import BotCommand

commands = [
    BotCommand(command='menu', description='главное меню'),
    BotCommand(command='games', description='Игровые платформы'),
    BotCommand(command='services', description='Оплата сервисов'),
    BotCommand(command='shop', description='Доставка товаров'),
    BotCommand(command='profile', description='Профиль'),
    BotCommand(command='cancel', description='Отмена'),
    BotCommand(command='start', description='start')
]
