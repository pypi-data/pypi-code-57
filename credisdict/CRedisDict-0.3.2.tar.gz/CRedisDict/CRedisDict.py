"""
Created on April 10 2020

@author: Joan Hérisson
"""

from sys import _getframe
from json import loads as json_loads
from json import dumps as json_dumps
from redis import Redis
from brs_utils import check_nb_args

class CRedisDict:
    """A redis based dict."""

    def __init__(self, name, redis, data={}):
        self.name = name
        self.redis = redis
        # This avoids to load all dict from redis each time we access to a key (often). So better than 'hmset'
        for key in data:
            self.__setitem__(key, data[key])

    def dict(self):
        d1 = self.redis.hgetall(self.name)
        d2 = {}
        for key in d1:
            d2[key] = json_loads(d1[key])
        return d2

    def keys(self):
        return self.redis.hkeys(self.name)

    @staticmethod
    def exists(redis, name):
        return redis.exists(name)

    def len(self):
        return self.redis.hlen(self.name)

    def is_empty(self):
        return self.len()==0

    def __iter__(self):
        return iter(self.keys())

    def __contains__(self, key):
        return self.redis.hexists(self.name, key)

    def __getitem__(self, key):
        item = self.redis.hget(self.name, key)
        # JSON for nested dictionnaries
        if item:
            return json_loads(item)
        else: raise KeyError

    def __setitem__(self, key, value):
        self.redis.hset(self.name, key, json_dumps(value))

    def __delitem__(self, key):
        return self.redis.hdel(self.name, key)

    def copy(self, *args):
        check_nb_args(*args, f_name=_getframe().f_code.co_name, nb_args=len(args))
        if isinstance(args[0], dict):
            for key in args[0]:
                self.__setitem__(key, args[0][key])
        elif isinstance(args[0], CRedisDict):
            # No need to copy data as there are already in redis
            self.__init__(args[0].name, args[0].redis)
        # self.name = redis_dict.name
        # self.redis = redis_dict.redis
        # for key in redis_dict.keys():
        #     self.__setitem__(key, redis_dict[key])

    def __eq__(self, *args):
        if len(args) < 1:
            raise TypeError(__eq__.name+' missing 1 required positional argument')
        elif len(args) > 1:
            raise TypeError(__eq__.name+' takes 1 positional arguments but '+len(args)+' were given')

        d = self.dict()
        if isinstance(args[0], dict):
            if d[key]!=args[0][key]:
                return False
        elif isinstance(args[0], CRedisDict):
            d_in = args[0].dict()
            # No need to copy data as there are already in redis
            if d[key]!=d_in[key]:
                return False

    def update(self, redis_dict):
        for field in redis_dict:
            self.__setitem__(field, redis_dict[field])
