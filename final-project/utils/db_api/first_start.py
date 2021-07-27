from asyncpg import Connection
from loader import db


async def db_create():
    pool: Connection = db
    """
        Таблица bot_chat
            chat_id ид чата
            chat_type тип чата (группа/супергруппа)
            bot_status присутствие бота в чате (True/False)
            chat_name имя чата
            is_admin является ли бот админом в этом чате? (True/False)
    """
    await pool.execute("""create table if not exists bot_chat
        (
            chat_id bigint not null,
            chat_type text not null,
            bot_status bool default FALSE,
            chat_name text,
            is_admin bool default FALSE,
            constraint bot_chat_pk
                primary key (chat_id)
        );

        create unique index if not exists bot_chat_chat_id_uindex
            on bot_chat (chat_id);""")

    """
    Общая база пользователей в чатах
        Таблица bot_chat
            id ид записи в бд
            user_id ид пользователя
            chat_id ид чата
            status статус пользователя (admin/member/left)
            first_name имя
            last_name фамилия
            username @юзернейм
            karma количество предупреждений
    """
    await pool.execute("""create table if not exists chat_users
        (
            id bigserial not null,
            user_id bigint not null,
            chat_id bigint not null,
            status text not null,
            first_name text,
            last_name text,
            username text,
            karma int not null default 0
        );
        
        create unique index if not exists chat_users_id_uindex
            on chat_users (id);""")

    # статистика пользователей
    await pool.execute("""create table if not exists statistics
        (
            user_id bigint not null,
            chat_id bigint not null,
            messages bigint default 0,
            ban_times int default 0,
            report int default 0
        );""")
