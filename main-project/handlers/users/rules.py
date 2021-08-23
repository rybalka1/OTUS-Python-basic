from aiogram import types
from loader import dp, db
from asyncpg import Record, Connection
from utils.misc import rate_limit


@rate_limit(1, "rules")
@dp.message_handler(
    commands="rules", chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]
)
async def bot_trigger_activate(message: types.Message):
    pool: Connection = db
    rules = await pool.fetchval(
        """SELECT rules FROM bot_chat where chat_id= $1""", message.chat.id
    )
    if rules:
        await message.reply(rules)
    else:
        await message.reply("Правила не установлены, используй /set_rule 1.2.3....")


@rate_limit(0, "set_rules")
@dp.message_handler(
    commands="set_rules",
    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    is_chat_admin=True,
)
async def bot_trigger_activate(message: types.Message):
    pool: Connection = db
    arg = message.chat.id, message.get_args()
    if await pool.fetchval(
        """UPDATE bot_chat SET rules=$2 WHERE chat_id=$1 RETURNING TRUE""", *arg
    ):
        await message.reply("Правила чата обновлены")
    else:
        await message.reply("Произошла ошибка при обновлении правил")
