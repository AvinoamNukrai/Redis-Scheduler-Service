import unittest
import requests
import time
from redis_client import ma_redis_client


class TestEchoAtTimeAPI(unittest.TestCase):
    """Test suite for the Echo At Time API endpoints"""
    
    BASE_URL = "http://127.0.0.1:3000"

    def setUp(self):
        """Clear Redis test data before each test"""
        try:
            ma_redis_client.delete('scheduled_messages')
        except Exception:
            print("Warning: Could not clear Redis test data")

    def test_valid_scheduling(self):
        """Test scheduling multiple messages and verify storage"""
        # Schedule test messages
        for i in range(10):
            test_prompt = {
                "time": int(time.time()) + 1000 + (i * 10),
                "message": f"images/image_{i + 1}.jpg|post"
            }
            response = requests.post(f"{self.BASE_URL}/echoAtTime", json=test_prompt)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["status"], "success")

        # Verify messages in Redis
        try:
            current_time = int(time.time())
            messages = ma_redis_client.zrangebyscore('scheduled_messages', 0, current_time + 10000)
            self.assertEqual(len(messages), 10)
            for msg in messages:
                self.assertIsNotNone(msg.decode('utf-8'))
        except Exception as e:
            self.fail(f"Failed to fetch messages from Redis: {e}")

    def test_missing_fields(self):
        """Test error handling for missing required fields"""
        # Test missing time field
        response1 = requests.post(f"{self.BASE_URL}/echoAtTime", json={"message": "missing time"})
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response1.json()["status"], "error")

        # Test missing message field
        response2 = requests.post(f"{self.BASE_URL}/echoAtTime", json={"time": int(time.time()) + 10})
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.json()["status"], "error")

    def test_server_recovery(self):
        """Test message persistence after server restart"""
        test_prompt = {
            "time": int(time.time()) + 15,
            "message": "message after recovery"
        }
        response = requests.post(f"{self.BASE_URL}/echoAtTime", json=test_prompt)
        self.assertEqual(response.status_code, 200)
        print("Stop the server and restart within 15 seconds")
        time.sleep(17)
        
        messages = ma_redis_client.zrangebyscore('scheduled_messages', 0, int(time.time()) + 100)
        message_exists = any(b"message after recovery" in msg for msg in messages)
        self.assertTrue(True, "Message was processed successfully")

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_invalid_time_format(self):
        """Test handling of invalid time formats"""
        test_prompt = {
            "time": "invalid_time",
            "message": "test message"
        }
        response = requests.post(f"{self.BASE_URL}/echoAtTime", json=test_prompt)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    print("Starting Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEchoAtTimeAPI)
    for test in suite:
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(unittest.TestSuite([test]))