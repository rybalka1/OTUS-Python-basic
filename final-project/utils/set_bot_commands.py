from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("set_rules", "Задать правила чата"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("rules", "Показать правила чата"),
        ],
        scope=types.BotCommandScopeAllChatAdministrators()
    )
    await dp.bot.set_my_commands(
        [
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("rules", "Показать правила чата"),
        ],
        scope=types.BotCommandScopeAllGroupChats()
    )
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить"),
            types.BotCommand("info", "Информация о боте"),
        ],
        scope=types.BotCommandScopeAllPrivateChats()
    )
