from aiogram import types
from loader import dp, db
from asyncpg import Record, Connection
from utils.misc import rate_limit


@rate_limit(1, "stats")
@dp.message_handler(
    commands="stats", chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]
)
async def bot_stats(message: types.Message):
    pool: Connection = db
    anws = f"""Статистика чата <b>{message.chat.title} </b>
    
Всего обработанно сообщений: <b>{await pool.fetchval('''SELECT sum(messages) FROM chat_users where chat_id= $1''', message.chat.id,)}</b>
Всего предупреждений: <b>{await pool.fetchval('''SELECT sum(karma) FROM chat_users where chat_id= $1''', message.chat.id,)}</b>
------------------------------------------
Сообщений от пользователя: <b>{message.from_user.full_name}: {await pool.fetchval('''SELECT messages FROM chat_users where chat_id= $1 and user_id=$2''', message.chat.id,message.from_user.id)}</b>
Получено предупреждений: <b>{await pool.fetchval('''SELECT karma FROM chat_users where chat_id= $1 and user_id=$2''', message.chat.id,message.from_user.id)}</b>"""
    await message.reply(anws)
