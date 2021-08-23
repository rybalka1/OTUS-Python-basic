from asyncpg import Connection
from loader import db


async def db_create():
    pool: Connection = db
    await pool.execute(
        """create table if not exists bot_chat
        (
            chat_id bigint not null,
            chat_type text not null,
            bot_status bool default FALSE,
            chat_name text,
            is_admin bool default FALSE,
            rules text,
            constraint bot_chat_pk
                primary key (chat_id)
        );

        create unique index if not exists bot_chat_chat_id_uindex
            on bot_chat (chat_id);"""
    )
    await pool.execute(
        """create table if not exists chat_users
        (
            id bigserial not null,
            user_id bigint not null,
            chat_id bigint not null,
            status text not null,
            first_name text,
            last_name text,
            username text,
            karma int not null default 0,
            messages bigint default 0,
            capcha bool default FALSE
        );
        
        create unique index if not exists chat_users_id_uindex
            on chat_users (id);"""
    )

    await pool.execute(
        """create table if not exists triggers
        (
            id serial not null,
            chat_id bigint,
            user_id bigint,
            tg_type text   not null,
            tg_text text,
            tg_audio text,
            tg_video text,
            tg_photo text,
            tg_name text,
            tg_animation text,
            tg_sticker text
        );

        create unique index if not exists triggers_chat_id_uindex
        on triggers (id);"""
    )
