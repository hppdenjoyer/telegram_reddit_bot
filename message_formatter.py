from typing import Dict
from config import MAX_POST_LENGTH


class MessageFormatter:
    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        """Escape special characters for Markdown V2"""
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text

    @staticmethod
    def format_post(post_data: Dict) -> tuple[str, str | None, bool]:
        """
        Format post data into a Telegram message
        Returns tuple of (formatted_text, media_url, is_video)
        """
        title = MessageFormatter.escape_markdown_v2(post_data['title'])
        text = MessageFormatter.escape_markdown_v2(post_data['text']) if post_data['text'] else ""
        media_url = post_data['media_url']
        is_video = post_data['is_video']

        # Create message text
        message_parts = [
            f"*{title}*",
            text if text else ""
        ]

        message = "\n\n".join(filter(None, message_parts))

        # Truncate if necessary
        if len(message) > MAX_POST_LENGTH:
            message = message[:MAX_POST_LENGTH - 3] + "\\.\\.\\."

        return message, media_url, is_video
