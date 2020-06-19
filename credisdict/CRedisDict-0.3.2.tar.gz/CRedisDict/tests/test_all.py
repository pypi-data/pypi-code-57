"""
Created on June 17 2020

@author: Joan Hérisson
"""

import unittest

from sys import path as sys_path
from sys import exit as sys_exit
sys_path.insert(0, '/home/src')
from CRedisDict import CRedisDict, wait_for_redis
from redis import StrictRedis

# Cette classe est un groupe de tests. Son nom DOIT commencer
# par 'Test' et la classe DOIT hériter de unittest.TestCase.
class TestCRedisDict(unittest.TestCase):

    def __init__(self, testname):
        super(TestCRedisDict, self).__init__(testname)
        self.redis = StrictRedis(host='db', port=6379, db=0, decode_responses=True)
        self.redis.flushall()

    # init() + dict()
    def test_initEmpty(self):
        self.redis.flushall()
        d = CRedisDict('d', self.redis)
        self.assertEqual(d.dict(), {})

    def test_initFromCRedisDict(self):
        self.redis.flushall()
        d1 = CRedisDict('d1', self.redis)
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        d2 = CRedisDict('d2', self.redis, d1)
        self.assertEqual(d1.dict(), d2.dict())

    def test_initFromDict(self):
        self.redis.flushall()
        d1 = {}
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        d2 = CRedisDict('d2', self.redis, d1)
        self.assertEqual(d2.dict(), d1)

    # keys()
    def test_keys(self):
        self.redis.flushall()
        d1 = CRedisDict('d1', self.redis)
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        self.assertEqual(d1.keys(), ['A', 'B', 'C'])

    # exists()
    def test_keys(self):
        self.redis.flushall()
        d1 = CRedisDict('d1', self.redis)
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        self.assertEqual(CRedisDict.exists(self.redis, 'd1'), True)
        self.assertEqual(CRedisDict.exists(self.redis, 'd2'), False)

    # len() + is_empty
    def test_keys(self):
        self.redis.flushall()
        d1 = CRedisDict('d1', self.redis)
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        self.assertEqual(d1.len(), 3)
        self.assertEqual(d1.is_empty(), False)
        d2 = CRedisDict('d2', self.redis)
        self.assertEqual(d2.len(), 0)
        self.assertEqual(d2.is_empty(), True)

    # update()
    def test_update(self):
        self.redis.flushall()
        d1 = {}
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        d1_r = CRedisDict('d1', self.redis, d1)
        d2 = {}
        d2['D'] = '4'
        d2['E'] = 'e'
        d2['F'] = {'d': 4, 'e': 5}
        d2_r = CRedisDict('d2', self.redis, d2)
        d2_r.update(d1_r)
        d2.update(d1)
        self.assertEqual(d2_r.dict(), d2)

    def test_addInt(self):
        self.redis.flushall()
        d = CRedisDict('d', self.redis)
        d['A'] = 1
        self.assertEqual(d['A'], 1)

    def test_addStr(self):
        self.redis.flushall()
        d = CRedisDict('d', self.redis)
        d['B'] = 'b'
        self.assertEqual(d['B'], 'b')

    def test_addDict(self):
        self.redis.flushall()
        d = CRedisDict('d', self.redis)
        d['C'] = {'a': 1, 'b': 2}
        self.assertEqual(d['C'], {'a': 1, 'b': 2})

    def test_copyCRedisDict(self):
        self.redis.flushall()
        d1 = CRedisDict('d1', self.redis)
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        d2 = d1
        self.assertEqual(d1.dict(), d2.dict())

    def test_copyDict(self):
        self.redis.flushall()
        d1 = {}
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        d2 = CRedisDict('d2', self.redis)
        d2.copy(d1)
        self.assertEqual(d2.dict(), d1)

    def test_equal(self):
        self.redis.flushall()
        d1 = {}
        d1['A'] = '1'
        d1['B'] = 'b'
        d1['C'] = {'a': 1, 'b': 2}
        d2 = CRedisDict('d2', self.redis, d1)
        self.assertEqual(d2.dict(), d1)
