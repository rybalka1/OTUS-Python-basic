import asyncpg
import logging

from data.config import PG_IP, PG_PASS, PG_USER, PG_DATABASE, PG_PORT

logging.basicConfig(
    format=u"%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
)


async def create_pool():
    return await asyncpg.create_pool(
        user=PG_USER, password=PG_PASS, host=PG_IP, database=PG_DATABASE, port=PG_PORT
    )
