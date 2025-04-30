from instagrapi import Client
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
    return username, password

def initialize_instagram_client():
    username, password = load_credentials('./credentials.txt')
    client = Client()
    client.login(username, password)
    return client

def test_post_to_instagram():
    client = initialize_instagram_client()
    content_path = "C:/Users/Avinoam Nukrai/Desktop/Insta-Agent/Redis-Scheduler-Service/images/image.jpg"
    
    if not os.path.exists(content_path):
        logger.error(f"File does not exist: {content_path}")
        return

    try:
        client.photo_upload(content_path, "Test post from script")
        logger.info("Post successful!")
    except Exception as e:
        logger.error(f"Failed to post: {e}")

if __name__ == "__main__":
    test_post_to_instagram() 