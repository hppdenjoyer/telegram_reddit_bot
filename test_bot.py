import asyncio
from telegram_bot import TelegramPoster
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def test_bot():
    poster = TelegramPoster()
    try:
        await poster.start_polling()
    except KeyboardInterrupt:
        await poster.reddit_client.close()


if __name__ == "__main__":
    asyncio.run(test_bot())
