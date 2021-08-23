from aiogram import types
from utils.misc.throttling import rate_limit
from loader import dp, db
from asyncpg import Connection, Record
from handlers.groups.service_messages import add_new_chat
from data.config import BOT_ID


@rate_limit(0, "echo_msg_users")
@dp.message_handler(
    content_types=types.ContentTypes.ANY,
    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
)
async def bot_new_all_chats_member(message: types.Message):
    pool: Connection = db
    await add_new_chat(
        message.chat.id,
        message.chat.type,
        True,
        message.chat.title,
        False
        if (await dp.bot.get_chat_member(message.chat.id, BOT_ID)).status == "member"
        else True,
    )
    if not message.from_user.is_bot:
        arg = message.chat.id, message.from_user.id
        member: Record = await pool.fetchrow(
            """SELECT * FROM chat_users WHERE chat_id=$1 AND user_id=$2""", *arg
        )
        if member:
            arg = (
                message.chat.id,
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
                (
                    await message.bot.get_chat_member(
                        message.chat.id, message.from_user.id
                    )
                )["status"],
            )
            await pool.fetchval(
                """UPDATE chat_users 
                                   SET status=$6, first_name=$4, last_name=$5, username=$3 
                                   WHERE chat_id= $1 AND user_id=$2""",
                *arg
            )
        else:
            arg = (
                message.from_user.id,
                message.chat.id,
                (
                    await message.bot.get_chat_member(
                        message.chat.id, message.from_user.id
                    )
                )["status"],
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
            )
            await pool.fetchval(
                """INSERT INTO chat_users (user_id, chat_id, status, first_name, last_name, username) 
                                   VALUES ($1,$2,$3,$4,$5,$6)""",
                *arg
            )
    arg = message.chat.id, message.from_user.id
    await pool.fetchval(
        """UPDATE chat_users SET messages=messages+1 WHERE user_id=$2 and chat_id=$1""",
        *arg
    )
