import pytest
from jtt_tm_utils.consul_handle import consul_reader
from jtt_tm_utils.redis_manager import redis_manager
import aioredis
async def test_read_redis():
    url =consul_reader.redis_as_url('master')
    print(url)

async def test_redismanager():
    await redis_manager.aload_configs(['master','slave','cache'])
    # print(redis_manager.master)
    # print(redis_manager.slave)
    slave =redis_manager.slave
    print(slave)