import time

from scrapy.utils.reqser import request_to_dict, request_from_dict

from shangyun_scrapy_lib.utils.requests import UpdateRequest
from shangyun_scrapy_lib.scrapy_redis import picklecompat


class Base(object):
    """Per-spider base queue class"""

    def __init__(self, server, spider, key, serializer=None):
        """Initialize per-spider redis queue.

        Parameters
        ----------
        server : StrictRedis
            Redis client instance.
        spider : Spider
            Scrapy spider instance.
        key: str
            Redis key where to put and get messages.
        serializer : object
            Serializer object with ``loads`` and ``dumps`` methods.

        """
        if serializer is None:
            # Backward compatibility.
            # TODO: deprecate pickle.
            serializer = picklecompat
        if not hasattr(serializer, 'loads'):
            raise TypeError("serializer does not implement 'loads' function: %r"
                            % serializer)
        if not hasattr(serializer, 'dumps'):
            raise TypeError("serializer '%s' does not implement 'dumps' function: %r"
                            % serializer)

        self.server = server
        self.spider = spider
        self.key = key % {'spider': spider.name}
        self.serializer = serializer

    def _encode_request(self, request):
        """Encode a request object"""
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
        """Push a request"""
        raise NotImplementedError

    def pop(self, timeout=0):
        """Pop a request"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)


class FifoQueue(Base):
    """Per-spider FIFO queue"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)
        if data:
            return self._decode_request(data)


class PriorityQueue(Base):
    """Per-spider priority queue abstraction using redis' sorted set"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.zcard(self.key)

    def push(self, request):
        """Push a request"""
        data = self._encode_request(request)
        score = -request.priority
        # We don't use zadd method as the order of arguments change depending on
        # whether the class is Redis or StrictRedis, and the option of using
        # kwargs only accepts strings, not bytes.
        self.server.execute_command('ZADD', self.key, score, data)

    def pop(self, timeout=0):
        """
        Pop a request
        timeout not support in this queue class
        """
        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])


class LifoQueue(Base):
    """Per-spider LIFO queue."""

    def __len__(self):
        """Return the length of the stack"""
        return self.server.llen(self.key)

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.blpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(self.key)

        if data:
            return self._decode_request(data)


class DelayQueue(Base):
    """延迟队列"""
    PREVIOUS = 5

    def __init__(self, *args, **kwargs):
        super(DelayQueue, self).__init__(*args, **kwargs)
        self.data_key = self.key + "_data"
        lua = """
            local ret = redis.call("zrangebyscore", KEYS[1], 0, ARGV[1], "LIMIT", 0, 1)
            if ret[1] then
                redis.call("zremrangebyrank", KEYS[1], 0, 0);
                return ret;
            end
            return nil;
        """
        self.pop_script = self.server.register_script(lua)

    def __len__(self):
        until_ts = int(time.time()) + self.PREVIOUS
        return self.server.zcount(self.key, 0, until_ts)

    def push(self, request: UpdateRequest):
        """
        :param data: data
        """
        # 唯一ID
        # task_id = str(uuid.uuid4())
        # save string
        # self.server.hset(self.data_key, task_id, )
        # add zset(queue_key=>data_key,ts)
        self.server.zadd(self.key, {self._encode_request(request): int(request.next_time)})

    def pop(self, timeout=10):
        """
        pop多条数据
        :param num: pop多少个
        :param previous: 获取多少秒前push的数据
        """
        # 取出previous秒之前push的数据
        until_ts = int(time.time()) - self.PREVIOUS
        result = self.pop_script(keys=[self.key], args=[until_ts])

        # 利用删除的原子性,防止并发获取重复数据
        # if count > 0 and task_id:
        # item = self.server.hget(self.data_key, task_id)
        # self.server.hdel(self.data_key, task_id)
        # return self._decode_request(item)
        # return None
        return self._decode_request(result[0]) if result else None


# TODO: Deprecate the use of these names.
SpiderQueue = FifoQueue
SpiderStack = LifoQueue
SpiderPriorityQueue = PriorityQueue
SpiderDelayQueue = DelayQueue
