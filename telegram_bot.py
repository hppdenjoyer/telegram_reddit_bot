import asyncio
import logging
from typing import Dict
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, CHECK_INTERVAL
from reddit_client import RedditClient
from message_formatter import MessageFormatter

logger = logging.getLogger(__name__)


class TelegramPoster:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        self.reddit_client = RedditClient()
        self.message_formatter = MessageFormatter()
        self.is_running = False

    async def send_post(self, post_data: Dict) -> None:
        """Send a single post to Telegram channel"""
        try:
            message_text, media_url, is_video = self.message_formatter.format_post(post_data)

            if media_url:
                try:
                    if is_video:
                        await self.bot.send_video(
                            chat_id=TELEGRAM_CHANNEL_ID,
                            video=media_url,
                            caption=message_text,
                            parse_mode=ParseMode.MARKDOWN_V2
                        )
                    else:
                        await self.bot.send_photo(
                            chat_id=TELEGRAM_CHANNEL_ID,
                            photo=media_url,
                            caption=message_text,
                            parse_mode=ParseMode.MARKDOWN_V2
                        )
                except Exception as e:
                    logger.warning(f"Failed to send media, falling back to text-only: {str(e)}")
                    # If sending with media fails, try sending text-only
                    await self.bot.send_message(
                        chat_id=TELEGRAM_CHANNEL_ID,
                        text=message_text,
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
            else:
                await self.bot.send_message(
                    chat_id=TELEGRAM_CHANNEL_ID,
                    text=message_text,
                    parse_mode=ParseMode.MARKDOWN_V2
                )

            logger.info(f"Successfully posted: {post_data['title']}")
            await asyncio.sleep(2)  # Добавляем задержку между постами

        except Exception as e:
            logger.error(f"Error sending post to Telegram: {str(e)}")
            if "Forbidden" in str(e):
                logger.error("Please ensure the bot is added to the channel as an administrator")
                self.is_running = False
            elif "Bad Request" in str(e):
                logger.error("Message formatting error, please check the Markdown syntax")
            elif "Too Many Requests" in str(e):
                logger.warning("Rate limit reached, increasing delay between posts")
                await asyncio.sleep(5)  # Увеличиваем задержку при достижении лимита

    async def process_new_posts(self) -> None:
        """Process new posts from Reddit"""
        if not self.is_running:
            return

        try:
            posts = await self.reddit_client.get_new_posts()
            for post in posts:
                await self.send_post(post)
                await asyncio.sleep(1)  # Avoid hitting rate limits
        except Exception as e:
            logger.error(f"Error processing posts: {str(e)}")

    async def start_polling(self) -> None:
        """Start the bot polling process"""
        try:
            await self.bot.send_message(
                chat_id=TELEGRAM_CHANNEL_ID,
                text="🤖 Reddit to Telegram Bot started\\!",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            logger.info("Bot started successfully")
            self.is_running = True
        except Exception as e:
            logger.error(f"Failed to send startup message: {str(e)}")
            if "Forbidden" in str(e):
                logger.error("Please ensure the bot is added to the channel as an administrator")
                return
            return

        try:
            while True:
                await self.process_new_posts()
                await asyncio.sleep(CHECK_INTERVAL)
        finally:
            await self.reddit_client.close()

async def main():
    poster = TelegramPoster()
    await poster.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())