# -*- coding: utf-8 -*-

import inspect
import functools
import itertools

import asyncio
import aioredis

from ifconf import configure_module, config_callback, configure_main

import logging
logger = logging.getLogger(__name__)

@config_callback
def config(loader):
    loader.add_attr('redis_uri_main', 'redis://localhost:6379/0?encoding=utf-8', help='redis uri to connect') # or uri 'unix:///path/to/redis/socket?db=1'
    loader.add_attr('redis_uri_logging', 'redis://localhost:6379/1?encoding=utf-8', help='redis uri to connect') # or uri 'unix:///path/to/redis/socket?db=1'

@config_callback('nds_file')
def nds_file_config(loader):
    loader.add_attr('attr_key_last_timestamp', 'nds_file_last_timestamp', help='redis key for last timestamp')
    loader.add_attr('attr_key_file_list', 'nds_file_list', help='redis key')
    loader.add_attr('attr_prefix_file_list_for_category', 'nds_file_list_category_{}', help='redis key')
    loader.add_attr('prefix_file_meta', 'nds_file_{}_{}', help='redis key')
    loader.add_attr('prefix_file_data', 'nds_file_{}_{}_data', help='redis key')

class RedisClient:

    def __init__(self, loop):
        self.conf = configure_module(config)
        self.loop = loop

    def load_nds_file_proxy(self):
        return NDSFileProxy(self)
            
    async def connect(self):
        self.conn = await aioredis.create_redis_pool(self.conf.redis_uri_main, minsize=1, maxsize=1)
        self.conn_for_subscription = await aioredis.create_redis_pool(self.conf.redis_uri_main, minsize=1, maxsize=1)
        self.conn_for_logging = await aioredis.create_redis_pool(self.conf.redis_uri_logging, minsize=1, maxsize=1)
        #self.main_conn_shared = await aioredis.create_redis_pool(self.conf.redis_uri_main)
        #self.main_conn_exclusive = await aioredis.create_redis_pool(self.conf.redis_uri_main, minsize=1, maxsize=20)
        #self.logging_conn = await aioredis.create_redis_pool(self.conf.redis_uri_logging)
        #logger.notice('CONNECTED|URL=%s'.format(self.main_conn_shared.address))
        logger.notice('CONNECTED|URL=%s', self.conn.address)

    async def connect_for_blocking(self, minsize, maxsize):
        return await aioredis.create_redis_pool(self.conf.redis_uri_main, minsize=minsize, maxsize=maxsize)

    def execute_threadsafe(self, func, *args, **kwargs):
        #raw_result = self.loop.call_soon_threadsafe(functools.partial(self.conn.execute, cmd, *args))
        async def wrap():
            ret = func(*args, **kwargs)
            if inspect.isawaitable(ret):
                return await ret
            else:
                return ret
        coro = func(*args, **kwargs) if inspect.iscoroutinefunction(func) else wrap()
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        while True:
            try:
                ret = future.result(10)
            except asyncio.TimeoutError as e:
                logger.warn('REDIS_EXECUTE_THREADSAFE|TIMEOUT|FUTURE=%s', future)
                continue
            except Exception as e:
                logger.exception('REDIS_EXECUTE_THREADSAFE|ERROR=%s', e)
                ret = -1
                break
            else:
                break
        return ret

    async def xadd(self, streamkey, *args, **kwargs):
        return await self.execute('XADD', streamkey, '*', *args, *itertools.chain.from_iterable(kwargs.items()))
        
    async def xadd_and_publish(self, pubkey, streamkey, *args, **kwargs):
        stream_id = await self.execute('XADD', streamkey, '*', *args, *itertools.chain.from_iterable(kwargs.items()))
        return await self.execute('PUBLISH', pubkey, stream_id)

    async def xlast_str(self, streamkey):
        ret = await self.execute_str('XREVRANGE', streamkey, '+', '-', 'COUNT', 1)
        return {v[0] : v[1] for v in zip(*[iter(ret[0][1])]*2)} if ret else {}
        
    async def psub_and_xrange_str(self, subkey, streamkey):
        ch = (await self.psubscribe(subkey))[0]
        logger.debug('PSUBSCRIBE|CHANNEL=%s', ch)
        last_id = '0'
        async for msg in ch.iter():
            logger.debug('PSUBSCRIBE|CHANNEL=%s|MSG=%s:%s', ch, msg[0], type(msg[1]))
            ret = await self.execute_str('XRANGE', streamkey, last_id+'1', '+')
            logger.debug('XRANGE|STREAM=%s|LAST_ID=%s|ret=%s', streamkey, last_id, ret)
            if ret is None:
                continue
            for result in ret:
                last_id = result[0]
                yield {v[0] : v[1] for v in zip(*[iter(result[1])]*2)} 
        
    async def psub_and_xrange_str_for_each_id(self, subkey, streamkey):
        ch = (await self.psubscribe(subkey))[0]
        logger.debug('PSUBSCRIBE|CHANNEL=%s', ch)
        async for msg in ch.iter():
            logger.debug('PSUBSCRIBE|CHANNEL=%s|MSG=%s:%s', ch, msg[0], msg[1])
            ret = await self.execute_str('XRANGE', streamkey, msg[1], msg[1])
            logger.debug('XRANGE|STREAM=%s|ID=%s|RET=%s', streamkey, msg, ret)
            if ret is None:
                continue
            for result in ret:
                yield {v[0] : v[1] for v in zip(*[iter(result[1])]*2)}
            
    #need to await
    def execute(self, cmd, *args):
        return self.conn.execute(cmd, *args, encoding=None)
            
    #need to await
    def execute_str(self, cmd, *args):
        return self.conn.execute(cmd, *args, encoding='UTF-8')
            
    #need to await
    def subscribe(self, key):
        return self.conn_for_subscription.subscribe(key)
        
    #need to await
    def unsubscribe(self, key_or_channel):
        return self.conn_for_subscription.unsubscribe(key_or_channel)
        
    #need to await
    def psubscribe(self, key):
        return self.conn_for_subscription.psubscribe(key)
        
    #need to await
    def punsubscribe(self, key_or_channel):
        return self.conn_for_subscription.punsubscribe(key_or_channel)
        
    
    async def close(self):
        self.conn_for_subscription.close()
        self.conn_for_logging.close()
        self.conn.close()
        await asyncio.gather(self.conn.wait_closed(), self.conn_for_logging.wait_closed(), self.conn_for_logging.wait_closed())
        logger.notice('CLOSED')

    async def blocking_command(self, coroutine):
        with await self.main_conn_exclusive as conn:
            await coroutine(conn)

    async def blocking_execute(self, cmd, *args):
        with await redis as r:
            await self.conn.execute(cmd, *args)

    
    async def get_and_wait(self, key):
        value = self.conn.get(key)
        if not value:
            ret = await conn.publish('test', key)


