import calendar
import logging
from datetime import datetime, timedelta
from aiogram.types import ChatType
from aiogram import types
from aiogram.utils.exceptions import NotEnoughRightsToRestrict
from asyncpg import Connection, Record

from loader import dp, db
from utils.misc import rate_limit


@rate_limit(1, "ro")
@dp.message_handler(
    chat_type=ChatType.GROUP,
    is_chat_admin=True,
    commands="ro",
    commands_prefix="!/",
    is_reply=True,
)
async def bot_no_ro(message: types.Message):
    await message.answer(
        "Данный чат не является супергруппой\nВыдача ограничений доступна только в супергруппе\n"
        "Что бы сделать чат супергруппой, необходимо назначить 5 или более админов"
    )


@rate_limit(1, "ro")
@dp.message_handler(
    commands_prefix="!/",
    chat_type=ChatType.SUPERGROUP,
    is_chat_admin=True,
    commands="ro",
    is_reply=True,
)
async def bot_ro(message: types.Message):
    status_user = (
        await message.bot.get_chat_member(
            message.chat.id, message.reply_to_message.from_user.id
        )
    )["status"]
    if status_user not in ["administrator", "creator"]:
        acc_right = True
        try:
            time_ban = int(message.text.split(" ", maxsplit=2)[1])
        except:
            time_ban = 1
        try:
            prichina = message.text.split(" ", maxsplit=2)[2]
        except:
            prichina = "причина не указана"
        dt_obj = datetime.now() + timedelta(hours=-3, minutes=time_ban)
        time_tuple = dt_obj.timetuple()
        timestamp_utc = calendar.timegm(time_tuple)
        who_ban = message.reply_to_message.from_user.id
        min_p = " min"
        try:
            await message.chat.restrict(
                who_ban, can_send_messages=False, until_date=timestamp_utc
            )
            await message.answer(f"Пользователь заблокирован на {time_ban}{min_p}")
        except NotEnoughRightsToRestrict:
            await message.reply(f"Недостаточно прав!")
            acc_right = False
        if acc_right:
            try:
                await message.bot.send_message(
                    who_ban,
                    (
                        f"Вы получили ограничение на общение в чате - {message.chat.title}\n"
                        f"Срок блокировки - {time_ban}{min_p}\n"
                        f"Причина - {prichina}"
                    ),
                )
            except Exception as e:
                logging.info(
                    f"Ошибка отправки уведомлению пользователю {who_ban} ошибка {e}"
                )
    else:
        await message.reply("Нельзя заблокировать администратора чата")


@rate_limit(1, "unro")
@dp.message_handler(
    chat_type=ChatType.GROUP,
    is_chat_admin=True,
    commands="unro",
    commands_prefix="!/",
    is_reply=True,
)
async def bot_no_unro(message: types.Message):
    await message.answer(
        "Данный чат не является супергруппой\nВыдача ограничений доступна только в супергруппе\n"
        "Что бы сделать чат супергруппой, необходимо назначить 5 или более админов"
    )


@rate_limit(1, "unro")
@dp.message_handler(
    commands_prefix="!/",
    chat_type=ChatType.SUPERGROUP,
    is_chat_admin=True,
    commands="unro",
    is_reply=True,
)
async def bot_unro(message: types.Message):
    dt_obj = datetime.now() + timedelta(hours=-3, minutes=0)
    time_tuple = dt_obj.timetuple()
    timestamp_utc = calendar.timegm(time_tuple)
    who_ban = message.reply_to_message.from_user.id
    await message.chat.restrict(
        message.reply_to_message.from_user.id,
        (await message.bot.get_chat(message.chat.id)).permissions,
        until_date=timestamp_utc,
    )
    await message.answer("Пользователь разблокирован")
    try:
        await message.bot.send_message(
            who_ban, "C вас сняты ограничения на общение в чате - " + message.chat.title
        )
    except Exception as e:
        logging.info(f"Ошибка отправки уведомлению пользователю {who_ban} ошибка {e}")


@rate_limit(1, "report")
@dp.message_handler(
    chat_type=[ChatType.GROUP, types.ChatType.SUPERGROUP],
    commands="report",
    is_reply=True,
    commands_prefix="!/",
)
async def bot_report(message: types.Message):
    pool: Connection = db
    get_chat_admins: Record = await pool.fetch(
        """SELECT * 
                                                  FROM chat_users 
                                                  WHERE status='administrator' OR status = 'creator';"""
    )
    for admin in get_chat_admins:
        msg = (
            f"Пользователь <a href='tg://user?id={message.from_user.id}'>"
            f"{message.from_user.full_name}</a> в чате <b>{message.chat.title}</b>\n"
            f"Жалуется на сообщение:\n"
            f"<code>{message.reply_to_message.text}</code>\n"
            f"от пользователя <a href='tg://user?id={message.reply_to_message.from_user.id}'>"
            f"{message.reply_to_message.from_user.full_name}</a>"
        )
        await message.bot.send_message(chat_id=admin["user_id"], text=msg)


@dp.message_handler(
    commands_prefix="!/",
    chat_type=[ChatType.SUPERGROUP, ChatType.GROUP],
    is_chat_admin=True,
    commands="warn",
    is_reply=True,
)
async def bot_warn(message: types.Message):
    pool: Connection = db
    warn = await pool.fetchval(
        """UPDATE chat_users 
                                  SET karma=(karma+1) 
                                  WHERE user_id=$1 AND chat_id=$2 RETURNING karma""",
        message.reply_to_message.from_user.id,
        message.chat.id,
    )
    if warn % 3 != 0:
        await message.reply(
            f"У пользователя {message.reply_to_message.from_user.full_name} {warn % 3}/3 предупреждений"
        )
    elif warn % 3 == 0 and warn > 0:
        dt_obj = datetime.now() + timedelta(hours=-3, minutes=60 * 24)
        time_tuple = dt_obj.timetuple()
        timestamp_utc = calendar.timegm(time_tuple)
        try:
            await message.chat.restrict(
                message.reply_to_message.from_user.id,
                can_send_messages=False,
                until_date=timestamp_utc,
            )
            await message.answer(f"Пользователь заблокирован на 1 день за 3 нарушения")
        except:
            pass
