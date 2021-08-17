from loader import dp, db
from asyncpg import Record, Connection
from utils.misc import rate_limit
from aiogram import types


@rate_limit(1, 'add_trigger')
@dp.message_handler(commands='trigger',
                    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    is_reply=True,
                    is_chat_admin=True,
                    commands_prefix='+')
async def bot_trigger_add_or_update(message: types.Message):
    if message.text != '+trigger':
        try:
            pool: Connection = db
            if message.reply_to_message.content_type == 'text':
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow(
                    '''SELECT tg_name FROM triggers WHERE tg_name = $1 and chat_id=$2''', *arg, )
                reply_text = message.reply_to_message.text
                arg = 'текст', name_trigger, reply_text, message.chat.id, message.from_user.id
                if find_tg:
                    if await pool.fetchval(
                            '''UPDATE triggers 
                            SET tg_text=$3,user_id=$5, tg_type=$1 
                            WHERE tg_name=$2 and user_id=$5 and chat_id = $4 RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список триггеров /triggers')
                else:
                    if await pool.fetchval(
                            '''INSERT INTO triggers (tg_type, tg_name , tg_text, chat_id, user_id) 
                            VALUES ($1,$2,$3,$4,$5) RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список триггеров /triggers')
            if message.reply_to_message.content_type == "animation":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow(
                    '''SELECT tg_name FROM triggers WHERE tg_name = $1 and chat_id=$2''', *arg, )
                reply_anim_id = message.reply_to_message.animation.file_id
                arg = 'гифка', name_trigger, reply_anim_id, message.chat.id, message.from_user.id
                if find_tg:
                    if await pool.fetchval(
                            '''UPDATE triggers 
                            SET tg_animation=$3,user_id=$5, tg_type=$1 
                            WHERE tg_name=$2 and user_id=$5 and chat_id = $4 RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список триггеров /triggers')
                else:
                    if await pool.fetchval(
                            '''INSERT INTO triggers (tg_type, tg_name , tg_animation, chat_id, user_id) 
                            VALUES ($1,$2,$3,$4,$5) RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список триггеров /triggers')
            if message.reply_to_message.content_type == "photo":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow(
                    '''SELECT tg_name FROM triggers WHERE tg_name = $1 and chat_id=$2''', *arg, )
                reply_photo_id = message.reply_to_message.photo[-1].file_id
                reply_caption = message.reply_to_message.caption
                arg = 'фото', name_trigger, reply_photo_id, message.chat.id, message.from_user.id, reply_caption
                if find_tg:
                    if await pool.fetchval(
                            '''UPDATE triggers 
                            SET tg_photo=$3,user_id=$5, tg_type=$1, tg_text=$6 
                            WHERE tg_name=$2 and user_id=$5 and chat_id = $4 RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список триггеров /triggers')
                else:
                    if await pool.fetchval(
                            '''INSERT INTO triggers (tg_type, tg_name , tg_photo, chat_id, user_id, tg_text) 
                            VALUES ($1,$2,$3,$4,$5,$6) RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список триггеров /triggers')
            if message.reply_to_message.content_type == "audio":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow(
                    '''SELECT tg_name FROM triggers WHERE tg_name = $1 and chat_id=$2''', *arg, )
                reply_audio_id = message.reply_to_message.audio.file_id
                reply_caption = message.reply_to_message.audio.title
                arg = 'аудио', name_trigger, reply_audio_id, message.chat.id, message.from_user.id, reply_caption
                if find_tg:
                    if await pool.fetchval(
                            '''UPDATE triggers 
                            SET tg_audio=$3,user_id=$5, tg_type=$1, tg_text=$6 
                            WHERE tg_name=$2 and user_id=$5 and chat_id = $4 RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список триггеров /triggers')
                else:
                    if await pool.fetchval(
                            '''INSERT INTO triggers (tg_type, tg_name , tg_audio, chat_id, user_id, tg_text) 
                            VALUES ($1,$2,$3,$4,$5,$6) RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список триггеров /triggers')
            if message.reply_to_message.content_type == "sticker":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow(
                    '''SELECT tg_name FROM triggers WHERE tg_name = $1 and chat_id=$2''', *arg, )
                reply_sticker_id = message.reply_to_message.sticker.file_id
                arg = 'стикер', name_trigger, reply_sticker_id, message.chat.id, message.from_user.id
                if find_tg:
                    if await pool.fetchval(
                            '''UPDATE triggers 
                            SET tg_sticker=$3,user_id=$5, tg_type=$1 
                            WHERE tg_name=$2 and user_id=$5 and chat_id = $4 RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список триггеров /triggers')
                else:
                    if await pool.fetchval(
                            '''INSERT INTO triggers (tg_type, tg_name , tg_sticker, chat_id, user_id) 
                            VALUES ($1,$2,$3,$4,$5) RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список триггеров /triggers')
            if message.reply_to_message.content_type == "video":
                name_trigger = message.text.split('trigger', maxsplit=1)[1].strip()
                arg = name_trigger, message.chat.id
                find_tg: Record = await pool.fetchrow(
                    '''SELECT tg_name FROM triggers WHERE tg_name = $1 and chat_id=$2''', *arg, )
                reply_video_id = message.reply_to_message.video.file_id
                reply_text = message.reply_to_message.caption
                arg = 'видео', name_trigger, reply_video_id, message.chat.id, message.from_user.id, reply_text
                if find_tg:
                    if await pool.fetchval(
                            '''UPDATE triggers 
                            SET tg_video=$3,user_id=$5, tg_type=$1, tg_text=$6 
                            WHERE tg_name=$2 and user_id=$5 and chat_id = $4 RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> обновлён!\n\nПросмотреть список триггеров /triggers')
                else:
                    if await pool.fetchval(
                            '''INSERT INTO triggers (tg_type, tg_name , tg_video, chat_id, user_id, tg_text) 
                            VALUES ($1,$2,$3,$4,$5,$6) RETURNING TRUE''',
                            *arg):
                        await message.answer(
                            f'триггер <b>{name_trigger}</b> добавлен!\n\nПросмотреть список триггеров /triggers')
        except:
            await message.answer('произошла ошибка')


@rate_limit(1, 'del_trigger')
@dp.message_handler(commands='trigger',
                    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    is_chat_admin=True,
                    commands_prefix='-')
async def bot_trigger_del(message: types.Message):
    if message.text != '-trigger':
        try:
            pool: Connection = db
            name_trigger = message.text.split('-trigger', maxsplit=1)[1].strip()
            arg = name_trigger, message.chat.id
            find_tg = await pool.fetchval('''SELECT id FROM triggers WHERE tg_name = $1 and chat_id=$2''', *arg, )
            if find_tg:
                if await pool.fetchrow('''delete from triggers WHERE id=$1 RETURNING TRUE''', find_tg, ):
                    await message.answer(f'триггер <b>{name_trigger}</b> был удалён')
                else:
                    await message.answer(f'Произошла ошибка, не смог удалить триггер {name_trigger}')
            else:
                await message.answer('Такого триггера не существует')
        except Exception as err:
            await message.answer(f'произошла ошибка {err}')


@rate_limit(2, 'trigger_list')
@dp.message_handler(commands='triggers',
                    chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    commands_prefix='/')
async def bot_trigger_list(message: types.Message):
    try:
        pool: Connection = db
        find_tg: Record = await pool.fetch('''SELECT tg_name, tg_type FROM triggers WHERE chat_id=$1''',
                                           message.chat.id, )
        list_tg = []
        if find_tg:
            for item in find_tg:
                list_tg.append(f'<b>{item["tg_name"]}</b>: {item["tg_type"]}')
            await message.answer(f'Список триггеров:\n' + "\n".join(list_tg))
        else:
            await message.answer(
                'Триггеры отсутствуют!\nЧто бы добавить триггер\n+trigger <b>имя триггера</b> ответом на сообщение')

    except Exception as err:
        await message.answer(f'произошла ошибка {err}')


@rate_limit(0, 'bot_trigger_activate')
@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
                    content_types=types.ContentTypes.TEXT, is_trigger=True)
async def bot_trigger_activate(message: types.Message):
    pool: Connection = db
    arg = message.chat.id, message.text
    trig: Record = await pool.fetchrow('''SELECT * from triggers where chat_id= $1 and tg_name = $2''', *arg)
    if trig["tg_type"] == 'текст':
        await message.answer(trig["tg_text"])
    elif trig["tg_type"] == 'гифка':
        await message.answer_animation(animation=trig["tg_animation"])
    elif trig["tg_type"] == 'фото':
        await message.answer_photo(photo=trig["tg_photo"], caption=trig["tg_text"])
    elif trig["tg_type"] == 'аудио':
        await message.answer_audio(audio=trig["tg_audio"], caption=trig["tg_text"])
    elif trig["tg_type"] == 'стикер':
        await message.answer_sticker(sticker=trig["tg_sticker"])
    elif trig["tg_type"] == 'видео':
        await message.answer_video(video=trig["tg_video"], caption=trig["tg_text"])
