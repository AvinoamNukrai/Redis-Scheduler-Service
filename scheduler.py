import time
from threading import Thread
from redis_client import ma_redis_client
from redis_storage import RedisStorage

redis_storage = RedisStorage(ma_redis_client) # our redis storage object

def start_scheduler():
    def scheduler():
        while True:
            try:
                # first we will extract all messages from the redis set s.t. their time <= current time
                all_messages = redis_storage.range_fetch_msgs(int(time.time()))
                for msg in all_messages:
                    lock_key = f"lock key: {msg.decode('utf-8')}"
                    # try locking for ensuring only 1 server process the msg
                    if redis_storage.locking(lock_key):
                        print(f"Executing message: {msg.decode('utf-8')}, time: {int(time.time())}") # important info
                        redis_storage.rm_msg(msg) # removing the message from the redis set cause she already handled
                        redis_storage.unlocking(lock_key) # release the lock after using
                time.sleep(1)
            except Exception as e:
                print(f"scheduler error due to: {e}")
                time.sleep(1)
    thread = Thread(target=scheduler)
    thread.daemon = True
    thread.start()
