import calendar
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from datetime import datetime, timedelta
import random
from asyncpg import Record, Connection


dat_antibot = CallbackData('antibot', 'action', 'awns', 'id')


async def antibot_cb_create(id, awns):
    kb = InlineKeyboardMarkup(row_width=5)
    cc = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    kk = []
    for item in range(0, 10):
        r = random.randint(0, len(cc) - 1)
        kk.append(cc[r])
        cc.pop(r)
    list_kb = []
    for item in kk:
        list_kb.append(InlineKeyboardButton(str(item), callback_data=dat_antibot.new(str(item), str(awns if awns == item else random.randint(55, 101)), str(id))))
        if len(list_kb) == 5:
            kb.add(*list_kb)
            list_kb = []
    return kb


@dp.callback_query_handler(dat_antibot.filter(action=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']))
async def inline_kb_antiflood(query: types.CallbackQuery, callback_data: dict):
    if query.from_user.id == int(callback_data["id"]):
        if callback_data['action'] == callback_data['awns']:
            dt_obj = datetime.now() + timedelta(hours=-3, minutes=0)
            time_tuple = dt_obj.timetuple()
            timestamp_utc = calendar.timegm(time_tuple)
            await query.bot.restrict_chat_member(query.message.chat.id, callback_data['id'], can_send_messages=True, until_date=timestamp_utc)
            await query.message.delete()
            pool: Connection = db
            arg = True, query.message.chat.id, query.from_user.id
            await pool.fetchval('''UPDATE chat_users SET capcha=$1 WHERE chat_id=$2 AND user_id=$3''', arg)
        else:
            await query.message.delete()