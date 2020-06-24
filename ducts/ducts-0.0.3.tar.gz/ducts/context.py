import concurrent

import ducts.redis
from ducts.event import HandlerManager

import logging
logger = logging.getLogger(__name__)

class ServerContext:

    def __init__(self, loop, ducts_home, max_workers = 1):
        self.loop = loop
        self.ducts_home = ducts_home
        self.redis = ducts.redis.RedisClient(self.loop)
        self.event_handler_manager = HandlerManager(self.ducts_home, self.loop, self.redis)
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

    def resolve_local_path(self, path):
        print('****************{}'.format(path))
        p = path.resolve() if path.is_absolute() else self.ducts_home.joinpath(path).resolve()
        print('****************{}'.format(p))
        return p

    def run_until_complete(self, future):
        return self.loop.run_until_complete(future)

    async def run_in_executor(self, func):
        return await self.loop.run_in_executor(self.thread_pool, func)

    def close(self):
        self.loop.run_until_complete(self.redis.close())
    
