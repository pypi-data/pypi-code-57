"""
   SDC Redis helper module
"""
import os
import redis

class RedisHelper:
    """
       Redis helper class
    """
    redis_conn = None
    def __init__(self, host: str = None, port: str = None, db: int = None):
        # temporary fix - these should be passed at init time
        if host is None:
            host = os.getenv('REDIS_HOST', 'localhost')
        # temporary fix - these should be passed at init time
        if port is None:
            port = int(os.getenv('REDIS_PORT', '6379'))
        # temporary fix - these should be passed at init time
        if db is None:
            db = int(os.getenv('REDIS_DB', '0'))
        try:
            self.redis_conn = redis.Redis(
                host=host,
                port=port,
                db=db
            )
        except redis.ConnectionError as exception:
            print(exception)

    def __del__(self):
        self.redis_conn.connection_pool.disconnect()

    def redis_set(self, *, key: str, value, expiry: int = None):
        """
            Set a Redis key with the specified value

            args:
                key (str): The Redis key
                value (str): The value to set
                expiry (int): A TTL for the specified key
        """
        self.redis_conn.set(key, value, expiry)

    def redis_get(self, *, key: str):
        """
            Get a Redis key

            args:
                key (str): The Redis key

            return:
                value : Returns the value for the specified key

        """
        return self.redis_conn.get(key)

    def redis_delete(self, *, key: str):
        """
            Delete a Redis key

            args:
                key (str): The Redis key

        """
        self.redis_conn.delete(key)

    def redis_hexists(self, *, hashkey: str):
        """Check hashkey exists in store"""
        return self.redis_conn.exists(hashkey)

    def redis_h_check_key_exists(self, *, hashkey: str, key: str):
        """Check key exists in haskey in store"""
        return self.redis_conn.hexists(hashkey, key)

    def redis_hmset(self, *, hashkey: str, dict_obj: dict):
        """Create or Overwrite dictionary hash store"""
        for key, val in dict_obj.items():
            self.redis_hset(hashkey=hashkey, key=key, value=val)

    def redis_hset(self, *, hashkey: str, key: str, value: str):
        """Create or Overwrite (key, value) pair in hash store"""
        self.redis_conn.hset(hashkey, key, value)

    def redis_hmget(self, *, hashkey: str, keys: list):
        """Read values for set of keys from hash store"""
        values = []
        for k in keys:
            values.append(self.redis_hget(hashkey=hashkey, key=k))
        return values

    def redis_hget(self, *, hashkey: str, key: str):
        """Read values for a given key from hash store"""
        return self.redis_conn.hget(hashkey, key)

    def redis_hmgetall(self, *, hashkey: str):
        """Read complete dict object from hash store"""
        return self.redis_conn.hgetall(hashkey)
