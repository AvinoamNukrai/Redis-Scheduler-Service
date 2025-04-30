import os
import random
import time
import logging
from instagrapi import Client
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_credentials(file_path):
    """
    Load the username and password for the automated account.
    :param file_path: Path to the credentials file.
    :return: Tuple of username and password.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
    return username, password

def initialize_instagram_client():
    """Initialize and login to Instagram account."""
    username, password = load_credentials('./credentials.txt')
    client = Client()
    client.login(username, password)
    return client

# Post media (either to the feed or as a story)
def post_content(client, content_path, is_story=False):
    """Post media (either to the feed or as a story)"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        if not os.path.exists(content_path):
            logger.info(f"File does not exist: {content_path}")
            return

        if is_story:
            if content_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                client.photo_upload_to_story(content_path)
                logger.info(f"Uploaded photo to story: {content_path}")
            elif content_path.lower().endswith('.mp4'):
                client.video_upload_to_story(content_path)
                logger.info(f"Uploaded video to story: {content_path}")
        else:
            client.photo_upload(content_path, f"chamonix, post at {current_time}")
            logger.info(f"Posted to feed: {content_path}")
    except Exception as e:
        logger.error(f"Failed to post content: {content_path}, error: {e}")

# Main function
def main():
    client = initialize_instagram_client()
    content_directory = "./images"

    # Run an infinite loop to keep posting every hour
    while True:
        # Iterate through all files in the directory
        for filename in os.listdir(content_directory):
            content_path = os.path.join(content_directory, filename)

            # Only proceed if the file is a valid media type (e.g., jpg, mp4)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4')):
                logger.info(f"Posting content: {content_path}")
                # If "story" in filename, post as a story
                # if "story" in filename.lower():
                post_content(client, content_path, is_story=True)
                # else:  # Otherwise, post to the feed
                post_content(client, content_path)

                # Wait for an hour before posting the next content
                logger.info("Waiting for 1 hour before the next post...")
                time.sleep(1800 + random.randint(1,10))  # Sleep for 1 hour (3600 seconds)

        # Optionally, logout after all posts and break the loop
        # client.logout()
        # break

if __name__ == "__main__":
    main()
