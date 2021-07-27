from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
PG_IP = env.str("PG_IP")
PG_PASS = env.str("PG_PASS")
PG_USER = env.str("PG_USER")
PG_DATABASE = env.str("PG_DATABASE")
PG_PORT = env.int("PG_PORT")
BOT_ID = BOT_TOKEN.split(':')[0]
