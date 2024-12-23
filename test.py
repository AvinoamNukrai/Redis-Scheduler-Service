import requests
import time
from redis_client import ma_redis_client



BASE_URL = "http://127.0.0.1:3000"

def valid_scheduling_test():
    print("Running test: valid Scheduling")
    for i in range(10):
        test_prompt = {"time":int(time.time()) + 100 + (i * 10), "message": f"message {i + 1}"}
        res = requests.post(f"{BASE_URL}/echoAtTime", json=test_prompt)
        print(f"scheduled message {i+1}: {res.json()}")

    print("\nFetching messages from Redis:")
    try:
        current_time = int(time.time())
        messages = ma_redis_client.zrangebyscore('scheduled_messages', 0, current_time + 10000)  # טווח של 100 שניות קדימה
        for msg in messages:
            print(f"Message in Redis: {msg.decode('utf-8')}")
    except Exception as e:
        print(f"Failed to fetch messages from Redis: {e}")


def missing_fields_test():
    print("Running test: Missing fields")
    res1 = requests.post(f"{BASE_URL}/echoAtTime", json={"message":"missing time"})
    print(f"Missing 'time': {res1.json()}")
    res2 = requests.post(f"{BASE_URL}/echoAtTime", json={"time": int(time.time()) + 10})
    print(f"Missing 'message': {res2.json()}")



def server_recovery_test():
    print("Running test: server recovery")
    test_prompt = {"time": int(time.time()) + 15,
                   "message": "message after recovery"}
    res = requests.post(f"{BASE_URL}/echoAtTime", json=test_prompt)
    print(f"Missing 'time': {res.json()}")
    print("stop now the server and restart within 15 seconds")
    time.sleep(17)


def health_test():
    print("Running test: health test")
    res = requests.post(f"{BASE_URL}/health") # should be 'get' and not 'post', the health method dosent support anything but 'get', only reading data requests from the server and nothing else (like sending data i.e. 'post')
    print(f"Health response: {res.json()}")




def run_tests():
    valid_scheduling_test()
    # missing_fields_test()
    # server_recovery_test()
    # health_test()

if __name__ == "__main__":
    print("Start Testing....")
    # run_tests()