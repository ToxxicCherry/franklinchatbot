from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='5702175370:AAE9yk5zdRuQqYeXVD89fctgvqxyqKrGXaw')
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)