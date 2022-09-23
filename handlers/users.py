from random import randint
from aiogram import types, Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class UserValidator(StatesGroup):
    user_number = State()


async def new_member(message: types.Message):
    global random_num
    random_num = randint(0, 9999)
    await message.reply(f'Привет! Проверка на бота. Отправь в чат число {random_num}')
    await UserValidator.user_number.set()


async def check_answer(message: types.Message, state: FSMContext):
    global random_num
    if random_num == int(message.text):
        await state.finish()
        return await message.reply('Ты справился с капчой!')
    else:
        return await message.reply('Ты не прошёл капчу!')


def register_handlers_users(dispatcher: Dispatcher):
    dispatcher.register_message_handler(new_member, content_types=[ContentType.NEW_CHAT_MEMBERS], state=None)
    dispatcher.register_message_handler(check_answer, state=UserValidator.user_number)
