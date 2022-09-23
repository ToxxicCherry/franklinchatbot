from random import randint
from create_bot import bot
from Scripts import CounterId
from aiogram import types, Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class UserValidator(StatesGroup):
    RANDOM_NUM = None
    user_number = State()


async def new_member(message: types.Message):
    UserValidator.RANDOM_NUM = randint(0, 9999)
    msg = await message.answer(f'Привет! Проверка на бота. Отправь в чат число {UserValidator.RANDOM_NUM}')
    global counter_id
    counter_id = CounterId()
    counter_id(msg.message_id)
    await UserValidator.user_number.set()


async def check_answer(message: types.Message, state: FSMContext):
    global counter_id
    if UserValidator.RANDOM_NUM == int(message.text):
        await state.finish()
        msg = await message.answer(f'{message.from_user.first_name} теперь с нами')
        counter_id(message.message_id)

        for msg_id in counter_id.ids:
            await bot.delete_message(chat_id='-1001716235924', message_id=msg_id)
    else:
        msg = await message.answer(f'{message.from_user.first_name} не прошёл капчу! Попробуй еще раз')
        counter_id(msg.message_id)
        counter_id(message.message_id)


def register_handlers_users(dispatcher: Dispatcher):
    dispatcher.register_message_handler(new_member, content_types=[ContentType.NEW_CHAT_MEMBERS], state=None)
    #dispatcher.register_message_handler(new_member, commands=['validate'], state=None)
    dispatcher.register_message_handler(check_answer, state=UserValidator.user_number)
