from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("set_rules", "Задать правила чата"),
            types.BotCommand("rules", "Показать правила чата"),
            types.BotCommand("ro", "Заблокировать пользователя"),
            types.BotCommand("unro", "Разблокировать пользователя"),
            types.BotCommand("triggers", "Список триггеров"),
            types.BotCommand("stats", "Статистика"),
            types.BotCommand("warn", "Выдать предупреждение"),
        ],
        scope=types.BotCommandScopeAllChatAdministrators()
    )
    await dp.bot.set_my_commands(
        [
            types.BotCommand("rules", "Показать правила чата"),
            types.BotCommand("triggers", "Список триггеров"),
            types.BotCommand("stats", "Статистика"),
        ],
        scope=types.BotCommandScopeAllGroupChats()
    )
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить"),
            types.BotCommand("help", "Информация о боте"),
        ],
        scope=types.BotCommandScopeAllPrivateChats()
    )
