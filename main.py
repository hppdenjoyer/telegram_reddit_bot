import asyncio
import logging
from telegram_bot import TelegramPoster

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main():
    poster = TelegramPoster()
    try:
        await poster.start_polling()
    except Exception as e:
        logging.error(f"Bot crashed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
