from aiogram import executor
from create_bot import dispatcher, bot
from handlers import users


async def on_startup(_):
    await bot.send_message('-1001716235924', 'Franklin v1.1.1 was started')

users.register_handlers_users(dispatcher=dispatcher)
executor.start_polling(dispatcher=dispatcher, skip_updates=True)