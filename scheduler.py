import time
import logging
from threading import Thread
from redis_client import ma_redis_client
from redis_storage import RedisStorage
from insta_posting import post_content, initialize_instagram_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_storage = RedisStorage(ma_redis_client) # our redis storage object

def start_scheduler():
    client = initialize_instagram_client() # Initialize Instagram client once

    def scheduler():
        while True:
            try:
                # Fetch all messages due for execution
                all_messages = redis_storage.range_fetch_msgs(int(time.time()))
                logger.info(f"Fetched {len(all_messages)} messages from Redis.")

                for msg in all_messages:
                    lock_key = f"lock key: {msg.decode('utf-8')}"
                    # Try locking to ensure only one server processes the message
                    if redis_storage.locking(lock_key):
                        # Parse the message to get content path and type (post/story)
                        content_path, is_story = parse_message(msg.decode('utf-8'))
                        logger.info(f"Attempting to post: {content_path}, as {'story' if is_story else 'post'}")
                        if content_path and is_story is not None:
                            post_content(client, content_path, is_story)
                            logger.info(f"Executed Instagram post: {content_path}, as {'story' if is_story else 'post'}, time: {int(time.time())}")
                            redis_storage.rm_msg(msg)
                        redis_storage.unlocking(lock_key)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Scheduler error due to: {e}")
                time.sleep(1)
    thread = Thread(target=scheduler)
    thread.daemon = True
    thread.start()

def parse_message(message):
    """Parse the message to extract content path and type (post/story)"""
    try:
        # Assuming message format is "content_path|is_story"
        parts = message.split('|')
        content_path = parts[0]
        is_story = parts[1].lower() == 'story'
        return content_path, is_story
    except IndexError:
        logger.error(f"Error parsing message: {message}. Expected format 'content_path|is_story'.")
        return None, None

if __name__ == "__main__":
    start_scheduler()
    while True:
        time.sleep(10)  # Keep the main thread alive
