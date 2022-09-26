from random import randint
from create_bot import bot
from DB import test_db
from Scripts import check_and_add, add_user_to_bd
from aiogram import types, Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class UserValidator(StatesGroup):
    user_number = State()


async def new_member(message: types.Message, state: FSMContext):
    random_num = str(randint(1000, 9999))
    msg = await message.reply(f'Привет! Проверка на бота. Отправь в чат число {random_num}')

    async with state.proxy() as data:
        data['msg'] = [msg.message_id]
        data['chat_id'] = message.chat.id
        data['random_num'] = random_num
        data['try_left'] = 3

    await UserValidator.user_number.set()


async def check_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['random_num'] == message.text:
            await state.finish()
            await message.answer(f'{message.from_user.first_name} теперь с нами')
            data['msg'].append(message.message_id)
            chat_id = data['chat_id']

            for msg_id in data['msg']:
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)

            user_id = message.from_user.id
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            user_name = message.from_user.username

            await check_and_add(message)
            await test_db(user_id, first_name, last_name, user_name)

        else:
            data['try_left'] -= 1
            if data['try_left'] == 0:
                await state.finish()
                await message.answer(f'{message.from_user.first_name} не прошел капчу и выгнан с позором!')
                data['msg'].append(message.message_id)

                for msg_id in data['msg']:
                    await bot.delete_message(chat_id='-1001716235924', message_id=msg_id)

            else:
                random_num = str(randint(1000, 9999))
                data['random_num'] = random_num
                msg = await message.reply(f'{message.from_user.first_name} не прошёл капчу!\n'
                                          f'Попыток осталось: {data["try_left"]}\n'
                                          f'Введи число {random_num}')
                data['msg'].append(msg.message_id)
                data['msg'].append(message.message_id)


async def add_user(message: types.Message):
    await check_and_add(message)


def register_handlers_users(dispatcher: Dispatcher):
    # dispatcher.register_message_handler(new_member, content_types=[ContentType.NEW_CHAT_MEMBERS], state=None)
    dispatcher.register_message_handler(new_member, commands=['validate'], state=None)
    dispatcher.register_message_handler(check_answer, state=UserValidator.user_number)
    dispatcher.register_message_handler(add_user, state=None)

