from config import DB_HOST, DB_USER, DB_PASSWORD, DATABASE, STEPIK_CHAT_ID
from aiogram import types
import asyncpg
import json


async def user_exists(user_id):
    try:
        async with asyncpg.create_pool(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DATABASE
        ) as pool:

            async with pool.acquire() as connection:
                result = await connection.fetch(f"""SELECT user_id FROM users WHERE user_id = {user_id}""")

    except Exception as ex:
        print(ex)
        print('Ошибка при проверке на существующего юзера')
    finally:
        if pool and connection:
            await pool.release(connection)
            return result


async def add_user_to_bd(user_id, first_name, last_name, user_name):
    try:
        async with asyncpg.create_pool(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DATABASE
        ) as pool:

            async with pool.acquire() as connection:
                await connection.execute(f"INSERT INTO "
                               f"users (user_id, first_name, last_name, user_name)"
                               f"VALUES ({user_id}, '{first_name}', '{last_name}','{user_name}');")

    except Exception as ex:
        print(ex)
        print('Ошибка при добавлении нового юзера')
    finally:
        if pool and connection:
            await pool.release(connection)


async def check_and_add(message: types.Message):
    if message.chat.id == STEPIK_CHAT_ID:
        user_id = message.from_user.id
        exist = await user_exists(user_id)

        if not exist:
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            user_name = message.from_user.username
            await add_user_to_bd(user_id=user_id, first_name=first_name, last_name=last_name, user_name=user_name)
            print(f'user {user_name} was added')


async def profanity_filter(message: types.Message):
    text = message.text.lower()

    with open('DB/profane.json', 'r') as file:
        data = json.load(file)

    result = any(map(lambda w: w['word'] in text, data))
    del data
    return result

