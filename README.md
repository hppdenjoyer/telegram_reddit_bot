# Reddit to Telegram Bot

Бот для автоматической публикации новых постов из выбранного сабреддита в Telegram канал. Бот отслеживает новые посты и публикует их содержимое (текст и изображения) в указанный Telegram канал.

## Возможности

- Автоматическое отслеживание новых постов в сабреддите
- Публикация текста и изображений в Telegram канал
- Защита от дублирования постов
- Поддержка форматирования Markdown
- Обработка ошибок и автоматическое восстановление соединения

## Требования

- Python 3.11 или выше
- Токен Telegram бота
- Учетные данные Reddit API
- ID Telegram канала

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd reddit-to-telegram-bot
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Создайте файл `.env` на основе `.env.example` и заполните необходимые переменные:
```env
Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id

Reddit Configuration
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=Reddit2TelegramBot/1.0
SUBREDDIT_NAME=your_subreddit_name

Application Configuration
CHECK_INTERVAL=60
```

## Настройка

### Получение токена Telegram бота
1. Обратитесь к [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте нового бота командой `/newbot`
3. Скопируйте полученный токен в `.env` файл

### Настройка Reddit API
1. Перейдите на [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Создайте новое приложение (тип: script)
3. Скопируйте Client ID и Client Secret в `.env` файл

### Получение ID канала Telegram
1. Добавьте бота в ваш канал как администратора
2. Возьмитее ID  канала в формате '@channel_name'
## Запуск

Запустите бота командой:
```bash
python main.py
```

Для тестового запуска используйте:
```bash
python test_bot.py
```

## Структура проекта

- `main.py` - основной файл запуска
- `telegram_bot.py` - логика работы с Telegram API
- `reddit_client.py` - клиент для работы с Reddit API
- `message_formatter.py` - форматирование сообщений
- `config.py` - конфигурация приложения
- `test_bot.py` - тестовый запуск

## Логирование

Бот ведет логи своей работы с различными уровнями важности:
- INFO - основные события
- WARNING - предупреждения
- ERROR - ошибки
- DEBUG - отладочная информация

## Устранение неполадок

1. **Бот не отправляет сообщения**
   - Проверьте права бота в канале
   - Убедитесь, что ID канала указан верно

2. **Не получает посты с Reddit**
   - Проверьте правильность учетных данных Reddit API
   - Убедитесь, что указано правильное имя сабреддита

3. **Дублируются посты**
   - Удалите файл `last_post.json` для сброса отслеживания
