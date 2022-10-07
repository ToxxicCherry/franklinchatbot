from random import randint
from create_bot import bot
from Scripts import check_and_add, profanity_filter
from config import ADMINS
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

            #await check_and_add(message) --- не работает
            #await test_db(user_id, first_name, last_name, user_name)

        else:
            data['try_left'] -= 1
            if data['try_left'] == 0:
                await state.finish()
                await message.answer(f'{message.from_user.first_name} не прошел капчу и получает бан\n'
                                     f'Может повторить попытку через час')
                await bot.ban_chat_member(chat_id=data['chat_id'], user_id=message.from_user.id, until_date=3600)

                data['msg'].append(message.message_id)
                for msg_id in data['msg']:
                    await bot.delete_message(chat_id=data['chat_id'], message_id=msg_id)

            else:
                random_num = str(randint(1000, 9999))
                data['random_num'] = random_num
                msg = await message.reply(f'{message.from_user.first_name} не прошёл капчу!\n'
                                          f'Попыток осталось: {data["try_left"]}\n'
                                          f'Введи число {random_num}')
                data['msg'].append(msg.message_id)
                data['msg'].append(message.message_id)


async def any_messages(message: types.Message):
    #await check_and_add(message) --- не работает
    if await profanity_filter(message):
        alert_message = ', '.join(ADMINS)
        alert_message = f'{alert_message}, в чате матерятся'
        await message.reply(alert_message)


def register_handlers_users(dispatcher: Dispatcher):
    dispatcher.register_message_handler(new_member, content_types=[ContentType.NEW_CHAT_MEMBERS], state=None)
    #dispatcher.register_message_handler(new_member, commands=['validate'], state=None)
    dispatcher.register_message_handler(check_answer, state=UserValidator.user_number)
    dispatcher.register_message_handler(any_messages, state='*')

