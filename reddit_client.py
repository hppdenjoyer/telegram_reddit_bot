import logging
from typing import Optional, Dict
import asyncpraw
from asyncpraw.models import Submission
import json
import os
import asyncio
from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    SUBREDDIT_NAME
)

logger = logging.getLogger(__name__)


class RedditClient:
    def __init__(self):
        self.reddit = asyncpraw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        self.subreddit = None
        self.last_post_id = None
        self.last_post_timestamp = 0
        self._load_last_post_id()

    def _load_last_post_id(self):
        """Load last processed post ID from file"""
        try:
            if os.path.exists('last_post.json'):
                with open('last_post.json', 'r') as f:
                    data = json.load(f)
                    self.last_post_id = data.get('last_post_id')
                    self.last_post_timestamp = data.get('last_post_timestamp', 0)
                    logger.info(f"Loaded last post ID: {self.last_post_id}")
        except Exception as e:
            logger.error(f"Error loading last post ID: {str(e)}")
            self.last_post_id = None
            self.last_post_timestamp = 0

    def _save_last_post_id(self):
        """Save last processed post ID to file"""
        try:
            with open('last_post.json', 'w') as f:
                json.dump({
                    'last_post_id': self.last_post_id,
                    'last_post_timestamp': self.last_post_timestamp
                }, f)
                logger.info(f"Saved last post ID: {self.last_post_id}")
        except Exception as e:
            logger.error(f"Error saving last post ID: {str(e)}")

    async def initialize(self):
        """Initialize subreddit connection with retry logic"""
        if not self.subreddit:
            max_retries = 3
            retry_delay = 5  # seconds

            for attempt in range(max_retries):
                try:
                    self.subreddit = await self.reddit.subreddit(SUBREDDIT_NAME)
                    logger.info(f"Successfully connected to subreddit: {SUBREDDIT_NAME}")
                    return
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Failed to connect to Reddit (attempt {attempt + 1}/{max_retries}): {str(e)}")
                        await asyncio.sleep(retry_delay)
                    else:
                        logger.error(f"Failed to connect to Reddit after {max_retries} attempts: {str(e)}")
                        raise

    async def _extract_media_url(self, submission: Submission) -> tuple[Optional[str], bool]:
        """
        Extract media URL from submission with error handling
        Returns tuple of (url, is_video)
        """
        try:
            # Check for Reddit-hosted video
            if submission.is_video and hasattr(submission, 'media'):
                try:
                    video_url = submission.media['reddit_video']['fallback_url']
                    return video_url, True
                except (KeyError, TypeError):
                    logger.debug(f"Failed to extract Reddit video URL from {submission.id}")

            # Check for image preview
            if hasattr(submission, 'preview'):
                return submission.preview['images'][0]['source']['url'], False

            # Check for direct image/video links
            if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                return submission.url, False
            if submission.url.endswith(('.mp4', '.webm')):
                return submission.url, True

        except (KeyError, IndexError, AttributeError) as e:
            logger.debug(f"No media found in submission {submission.id}: {str(e)}")
        return None, False

    async def get_new_posts(self) -> list[Dict]:
        """
        Fetch new posts from the subreddit with improved error handling
        Returns a list of dictionaries containing post data
        """
        try:
            await self.initialize()
            posts = []

            try:
                async for submission in self.subreddit.new(limit=5):
                    if self.last_post_id and submission.id == self.last_post_id:
                        break

                    if self.last_post_id and submission.created_utc <= self.last_post_timestamp:
                        continue

                    try:
                        media_url, is_video = await self._extract_media_url(submission)
                        post_data = {
                            'id': submission.id,
                            'title': submission.title,
                            'text': submission.selftext,
                            'media_url': media_url,
                            'is_video': is_video,
                            'created_utc': submission.created_utc
                        }
                        posts.append(post_data)
                        logger.debug(f"Processed post {submission.id}")
                    except Exception as e:
                        logger.error(f"Error processing post {submission.id}: {str(e)}")
                        continue

                if posts:
                    self.last_post_id = posts[0]['id']
                    self.last_post_timestamp = posts[0]['created_utc']
                    self._save_last_post_id()
                    logger.info(f"Found {len(posts)} new posts")
                else:
                    logger.info("No new posts found")

                return posts

            except asyncpraw.exceptions.PRAWException as e:
                logger.error(f"Reddit API error: {str(e)}")
                return []

        except Exception as e:
            logger.error(f"Error fetching Reddit posts: {str(e)}")
            return []

    async def close(self):
        """Close the Reddit client connection"""
        try:
            await self.reddit.close()
            logger.info("Reddit client connection closed")
        except Exception as e:
            logger.error(f"Error closing Reddit client: {str(e)}")
