class RedisStorage:
    """
    class for redis object, containing the redis client and sorted set, enabling add/remove/get range messages/lock/unlock mutexes
    """
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def store_msg(self, msg, exec_time):
        self.redis_client.zadd('scheduled_messages', {msg: exec_time})

    def range_fetch_msgs(self, curr_time):
        return self.redis_client.zrangebyscore('scheduled_messages', 0, curr_time)

    def rm_msg(self, msg):
        self.redis_client.zrem('scheduled_messages', msg)

    def locking(self, lock_key, timeout=10):
        if self.redis_client.setnx(lock_key, "locked"):
            self.redis_client.expire(lock_key, timeout)
            return True
        return False

    def unlocking(self, lock_key):
        self.redis_client.delete(lock_key)