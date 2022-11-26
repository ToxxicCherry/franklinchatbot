from aiogram import executor, types
from create_bot import dispatcher, bot
from handlers import users
from config import STEPIK_CHAT_ID



async def on_startup(_):
    await bot.send_message(STEPIK_CHAT_ID, 'Franklin was started in test mode')



call = types.CallbackQuery()
users.register_handlers_users(dispatcher=dispatcher)
executor.start_polling(dispatcher=dispatcher, skip_updates=True)