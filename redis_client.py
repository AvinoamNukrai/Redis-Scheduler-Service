import redis
import json

# Load configuration
with open('appsettings.json') as config_file:
    config = json.load(config_file)


# Initiate redis client
def create_redis_client():
    try:
        client = redis.StrictRedis(host=config['Redis']['ConnectionString'])
        # Test the connection
        client.ping()
        return client
    except:
        raise RuntimeError("Redis server is not running. Please start the Redis server and try again.")


ma_redis_client = create_redis_client()




