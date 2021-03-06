# Проектная работа по курсу "Python Developer. Basic"

## Тема проектной работы: "Telegram-бот, помощник по администрированию telegram-групп"

## Описание

Телеграм-бот для адинистрирования групп в телеграм-каналах. Умеет запоминать пользователей, приветствовать, сообщать о правилах группы и о нарушении правил.

## Запуск проекта

Создаем виртуальное окружение:

```shell
python3 -m venv .venv
```

Активируем виртуально окружение:

```shell
 source .venv/bin/activate
```

Устанавливаем зависимости:

```shell
pip3 install -r requirements.txt
```

Создаём файл `.env` в корневой папке проекта, как образец можно использовать файл `.env.dist`:

```shell
cp .env.dist .env
```

Заполняем поля:

- ADMINS
- BOT_TOKEN
- PG_IP
- PG_PASS
- PG_USE
- PG_DATABASE
- PG_PORT

Запускаем приложение:

```shell
python3 app.py
```
