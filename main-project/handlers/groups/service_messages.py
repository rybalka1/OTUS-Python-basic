import logging
import random
import calendar
from datetime import datetime, timedelta

from aiogram import types

from keyboards.inline.anti_bot import antibot_cb_create
from loader import dp, db
from asyncpg import Record, Connection
from data.config import BOT_ID


async def add_new_chat(*args):
    pool: Connection = db
    chat_find: Record = await pool.fetchval('''SELECT chat_id FROM bot_chat WHERE chat_id= $1''', args[0], )
    if not chat_find:
        await pool.fetchval('''INSERT INTO bot_chat VALUES ($1,$2,$3,$4,$5)''', *args)
        logging.info(f'Добавлен чат\nid: {args[0]}\ntitle: {args[3]}\ntype: {args[1]}\npermissions: {args[4]}')
        return False
    else:
        return True


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def bot_new_all_chats_member(message: types.Message):
    pool: Connection = db
    await add_new_chat(message.chat.id, message.chat.type, True, message.chat.title,
                       False if (await dp.bot.get_chat_member(message.chat.id, BOT_ID)).status == 'member' else True)
    for item in message.new_chat_members:
        if not item.is_bot:
            arg = message.chat.id, item.id
            member: Record = await pool.fetchrow(
                '''SELECT * 
                FROM chat_users 
                WHERE chat_id= $1 AND user_id=$2''', *arg)
            if member:
                arg = item.id, message.chat.id, 'member', item.first_name, item.last_name, item.username
                await pool.fetchval(
                    '''UPDATE chat_users
                    SET status=$3, first_name=$4, last_name=$5, username=$6 
                    WHERE chat_id=$2 AND user_id=$1''', *arg)
                await message.answer(f'{member.get("last_name")} {member.get("first_name")} с возвращением!')
                if not member["capcha"]:
                    dt_obj = datetime.now() + timedelta(hours=-3, days=365)
                    time_tuple = dt_obj.timetuple()
                    timestamp_utc = calendar.timegm(time_tuple)
                    await message.chat.restrict(item.id,
                                                permissions=(await message.bot.get_chat(message.chat.id)).permissions,
                                                until_date=timestamp_utc)
                    rd = random.randint(1, 10)
                    txt = f'Это антибот защита, выбери {rd}'
                    await message.answer(text=txt, reply_markup=await antibot_cb_create(item.id, rd))
            else:
                arg = item.id, message.chat.id, 'member', item.first_name, item.last_name, item.username, 0
                await pool.fetchval('''
                    INSERT INTO chat_users (user_id, chat_id, status, first_name, last_name, username, karma)
                    VALUES ($1,$2,$3,$4,$5,$6,$7)''', *arg)
                await message.answer(f'{item.first_name} {member.get("first_name")} ну, допустим, привет!')
                dt_obj = datetime.now() + timedelta(hours=-3, days=365)
                time_tuple = dt_obj.timetuple()
                timestamp_utc = calendar.timegm(time_tuple)
                await message.chat.restrict(item.id, permissions=(await message.bot.get_chat(message.chat.id)).permissions, until_date=timestamp_utc)
                rd = random.randint(1, 10)
                txt = f'Это антибот защита, выбери {rd}'
                await message.answer(text=txt, reply_markup=await antibot_cb_create(item.id, rd))


@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def bot_left_all_chats_member(message: types.Message):
    pool: Connection = db
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f'{message.left_chat_member.full_name} покинул нас!')
    elif message.from_user.id == BOT_ID:
        return
    else:
        await message.answer(f'{message.left_chat_member.full_name} кикнут из чата '
                             f'администратором {message.from_user.get_mention(as_html=True)}')

    await add_new_chat(message.chat.id, message.chat.type, True, message.chat.title,
                       False if (await dp.bot.get_chat_member(message.chat.id, BOT_ID)).status == 'member' else True)
    arg = message.chat.id, message.left_chat_member.id
    member: Record = await pool.fetchrow('''SELECT * 
                                            FROM chat_users 
                                            WHERE chat_id= $1 AND user_id=$2''', *arg)
    if not message.left_chat_member.is_bot:
        if member:
            arg = (message.chat.id, message.left_chat_member.id, message.left_chat_member.username,
                   message.left_chat_member.first_name, message.left_chat_member.last_name, 'left')
            await pool.fetchval(
                '''UPDATE chat_users 
                SET username=$3, first_name=$4, last_name=$5, status=$6  
                WHERE chat_id= $1 AND user_id=$2''', *arg)
        else:
            arg = (message.left_chat_member.id, message.chat.id, 'left',
                   message.left_chat_member.first_name, message.left_chat_member.last_name,
                   message.left_chat_member.username)
            await pool.fetchval('''
                INSERT INTO chat_users (user_id, chat_id, status, first_name, last_name, username)
                VALUES ($1,$2,$3,$4,$5,$6)''', *arg)


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_TITLE)
async def bot_new_chat_title(message: types.Message):
    pool: Connection = db
    if not await add_new_chat(message.chat.id, message.chat.type, True, message.chat.title,
                              False if (await dp.bot.get_chat_member(message.chat.id,
                                                                     BOT_ID)).status == 'member' else True):
        arg = message.chat.id, message.new_chat_title
        await pool.fetchval('''UPDATE bot_chat 
                               SET chat_name=$2 
                               WHERE chat_id=$1''', *arg)


@dp.message_handler(content_types=types.ContentTypes.MIGRATE_TO_CHAT_ID)
async def bot_new_chat_title(message: types.Message):
    pool: Connection = db
    if not await add_new_chat(message.chat.id, message.chat.type, True, message.chat.title,
                              False if (await dp.bot.get_chat_member(message.chat.id,
                                                                     BOT_ID)).status == 'member' else True):
        arg = message.chat.id, message.migrate_to_chat_id, message.chat.type
        await pool.fetchval('''UPDATE bot_chat SET chat_id=$2, chat_type=$3 WHERE chat_id=$1''', *arg)
        arg = message.chat.id, message.migrate_to_chat_id
        await pool.fetchval('''UPDATE chat_users SET chat_id=$2 WHERE chat_id=$1''', *arg)
        await pool.fetchval('''UPDATE triggers SET chat_id=$2 WHERE chat_id=$1''', *arg)


@dp.message_handler(content_types=types.ContentTypes.MIGRATE_FROM_CHAT_ID)
async def bot_new_chat_title(message: types.Message):
    pool: Connection = db
    if not await add_new_chat(message.chat.id, message.chat.type, True, message.chat.title,
                              False if (await dp.bot.get_chat_member(message.chat.id,
                                                                     BOT_ID)).status == 'member' else True):
        arg = message.migrate_from_chat_id, message.chat.id, message.chat.type
        await pool.fetchval('''UPDATE bot_chat SET chat_id=$2, chat_type=$3 WHERE chat_id=$1''', *arg)
        arg = message.migrate_from_chat_id, message.chat.id
        await pool.fetchval('''UPDATE chat_users SET chat_id=$2 WHERE chat_id=$1''', *arg)
        await pool.fetchval('''UPDATE triggers SET chat_id=$2 WHERE chat_id=$1''', *arg)
