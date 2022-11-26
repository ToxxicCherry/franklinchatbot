from aiogram import Bot
import os
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='5254925799:AAEymQkApKaGzcft_iynZH0Pfa3ZMLmDnkE')
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)