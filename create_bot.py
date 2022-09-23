from aiogram import Bot
import os
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=os.getenv('TOKEN'))
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)