from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), chat_type=types.ChatType.PRIVATE)
async def bot_help(message: types.Message):
    text = (f"Привет {message.from_user.full_name}",
            "Я бот который помогает блюсти порядок в чатах",
            "Что бы начать работать со мной, просто добавь меня в чат")
    
    await message.answer("\n".join(text))
