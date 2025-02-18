import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

# Reddit Configuration
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'Reddit2TelegramBot/1.0')
SUBREDDIT_NAME = os.getenv('SUBREDDIT_NAME')

# Application Configuration
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))  # seconds
MAX_POST_LENGTH = 4096  # Telegram message length limit
