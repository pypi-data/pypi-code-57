import asyncio
import datetime
import enum
import logging
import unittest
import os
from unittest import mock

import pyemit.emit as e
from pyemit.remote import Remote
from tests.helper import async_test

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

_received_test_decorator_msgs = 0


@e.on('test_decorator')
async def on_test_decorator(msg):
    global _received_test_decorator_msgs
    logger.info("on_test_decorator")
    _received_test_decorator_msgs += 1


def check_log(log_func, msg: str):
    for call in log_func.call_args.call_list():
        if call.find(msg) != -1:
            return True
    return False


class MyEnum(enum.Enum):
    MONDAY = 0


class Sum(Remote):
    def __init__(self, to_be_sum):
        super().__init__()
        self.timestamp = datetime.datetime.now()
        self.start = MyEnum.MONDAY
        self.to_be_sum = to_be_sum

    async def server_impl(self, *args, **kwargs):
        result = sum(self.to_be_sum)
        await super().respond(result)


class TestEmit(unittest.TestCase):
    def setUp(self) -> None:
        self.echo_times = 0
        self.dsn = "redis://localhost"

    def tearDown(self) -> None:
        asyncio.run(e.stop())

    @async_test
    async def test_decorator(self):
        await e.start(e.Engine.REDIS, dsn=self.dsn, start_server=True)
        logger.info(f"{e._registry}")
        await e.emit("test_decorator")
        await asyncio.sleep(0.2)
        self.assertEqual(_received_test_decorator_msgs, 1)

    async def on_in_process(self, msg):
        # self.assertEqual(msg, "in-process")
        print(msg)

    @async_test
    async def test_in_process_engine(self):
        e.register('test_in_process', self.on_in_process)
        await e.start(e.Engine.IN_PROCESS)
        e.register("test_after_start", self.on_in_process)

        await asyncio.sleep(0.1)
        await e.emit('test_in_process', {"msg": "in-process"})
        await e.emit("test_after_start", {"msg": "after-start"})
        await asyncio.sleep(0.5)

    async def on_echo(self, msg):
        logger.info("on_echo received: %s", msg)
        self.echo_times += 1
        if self.echo_times < 1:
            await e.emit('echo', msg)

    @async_test
    async def test_aio_redis_engine(self):
        await e.start(e.Engine.REDIS, dsn=self.dsn, start_server=True)
        e.register('echo', self.on_echo)

        await asyncio.sleep(0.5)
        await e.emit('echo', {"msg": "new message 1.0"})
        # receiver will receive None
        await e.emit('echo')
        # this will cause no problem. sender can send any message out
        await e.emit("not registered")
        await asyncio.sleep(1)

    @async_test
    async def test_heart_beat(self):
        e.register("hi", self.on_echo)
        await e.start(e.Engine.REDIS, heart_beat=0.5, dsn=self.dsn, start_server=True)
        await asyncio.sleep(1)

    @async_test
    async def test_redis_rpc_call(self):
        await e.start(e.Engine.REDIS, dsn=self.dsn, start_server=True, exchange='unittest')
        foo = Sum([0, 1, 2])
        print(foo)
        response = await foo.invoke()
        self.assertEqual(3, response)

        await asyncio.sleep(0.1)

    @async_test
    async def test_inprocess_rpc_call(self):
        await e.start(exchange='unittest')
        foo = Sum([0, 1, 2, 3, 4])
        response = await foo.invoke()
        self.assertEqual(10, response)

        await asyncio.sleep(0.1)

    @async_test
    async def test_inprocess_stop(self):
        e.register("test_stop", self.on_echo)
        await e.start()
        await e.stop()

    @async_test
    async def test_redis_stop(self):
        e.register("test_stop", self.on_echo)
        await e.start(e.Engine.REDIS, heart_beat=0.3, start_server=True, dsn=self.dsn)

        await e.emit("test_stop", {"msg": "check this in log"})
        await asyncio.sleep(0.1)
        e.unsubscribe("test_stop", self.on_echo)
        await e.emit("test_stop", {"msg": "nobody will handle this"})

    @async_test
    async def test_unsubscribe(self):
        e.register("test_unsub", self.on_echo)
        self.assertIn(self.on_echo, e._registry['/test_unsub']['handlers'])
        await e.start()
        e.unsubscribe("test_unsub", self.on_echo)
        self.assertNotIn(self.on_echo, e._registry['/test_unsub']['handlers'])

        e.register('test_unsub', self.on_echo)
        logger = logging.getLogger('pyemit.emit')
        logger.warning = mock.MagicMock(name='warning')
        e.unsubscribe('test_unsub', self.test_unsubscribe)
        self.assertTrue(check_log(logger.warning, 'is not registered as handler of'))

    @async_test
    async def test_error_handling(self):
        # handler is not registered
        await e.start()

        logger = logging.getLogger('pyemit.emit')
        logger.warning = mock.MagicMock(name='warning')
        await e.emit("test_not_registered")
        self.assertTrue(check_log(logger.warning, 'test_not_registered has no listener'))

        # ConnectionClosedError when publish
        await e.stop()
        await e.start(e.Engine.REDIS, dsn=self.dsn)
        e._pub_conn.publish = mock.MagicMock()
        import aioredis
        e._pub_conn.publish.side_effect = aioredis.errors.ConnectionClosedError()
        e.register('mock_connection_closed', self.on_echo)
        try:
            await e.emit("this should raise connectionclosederror")
            self.assertTrue(False)
        except ConnectionError as error:
            logger.exception(error)
            self.assertTrue(True)
