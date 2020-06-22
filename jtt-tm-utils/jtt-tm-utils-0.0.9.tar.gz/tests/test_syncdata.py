from jtt_tm_utils.sync_basedata import data_manager
import aioredis
import os
import asyncio

import unittest

class CliTestCase(unittest.TestCase):
    def setUp(self):
        async def _setup():
            redis = await aioredis.create_redis_pool('redis://192.168.101.70:6380/0')
            data_manager.config(redis)
            #
        self.loop =asyncio.get_event_loop()
        self.loop.run_until_complete(_setup())


    # def test_up_project(self):
    #     os.chdir(os.path.join(self.projectname))
    #     up_project()


    def test_makemethod(self):
       self.loop.run_until_complete( data_manager.get_vehicle('110-FX'))


