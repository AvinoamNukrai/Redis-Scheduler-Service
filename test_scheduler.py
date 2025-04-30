import unittest
from unittest.mock import patch, MagicMock
from scheduler import parse_message, start_scheduler
from redis_storage import RedisStorage
import time

class TestScheduler(unittest.TestCase):
    def setUp(self):
        # Mock RedisStorage
        self.redis_storage_mock = MagicMock(spec=RedisStorage)
        self.redis_storage_mock.range_fetch_msgs.return_value = [
            b"./images/image.jpg|post",
            b"./images/image.jpg|story"
        ]

    def test_parse_message(self):
        # Test valid message parsing
        content_path, is_story = parse_message("path/to/image.jpg|story")
        self.assertEqual(content_path, "path/to/image.jpg")
        self.assertTrue(is_story)

        content_path, is_story = parse_message("path/to/image.jpg|post")
        self.assertEqual(content_path, "path/to/image.jpg")
        self.assertFalse(is_story)

        # Test invalid message parsing
        content_path, is_story = parse_message("invalid_message_format")
        self.assertIsNone(content_path)
        self.assertIsNone(is_story)

    @patch('scheduler.post_content')
    @patch('scheduler.initialize_instagram_client')
    def test_scheduler_execution(self, mock_initialize_instagram_client, mock_post_content):
        # Mock Instagram client
        mock_client = MagicMock()
        mock_initialize_instagram_client.return_value = mock_client

        # Start the scheduler in a separate thread
        with patch('scheduler.redis_storage', self.redis_storage_mock):
            start_scheduler()
            time.sleep(2)  # Allow some time for the scheduler to run

        # Verify that post_content was called with the correct arguments
        mock_post_content.assert_any_call(mock_client, "path/to/image1.jpg", False)
        mock_post_content.assert_any_call(mock_client, "path/to/image2.jpg", True)

if __name__ == "__main__":
    unittest.main() 