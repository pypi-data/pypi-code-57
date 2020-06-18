# -*- coding: utf-8 -*-
"""
Basic redis connector
"""
import json
from typing import Union, List, Dict, Any, Optional

import redis

from nosqlmodel.connectors.baseconnector import BaseNosqlConnector

__author__ = 'ozgur'
__creation_date__ = '9.09.2019' '10:07'

RHOST: str = "localhost"
RPORT: int = 6379


class RedisConnector(BaseNosqlConnector):
    """Redis connector for models. Can also be used as standalone lib too"""

    def __init__(self, dbnum: int = 0, host=RHOST, port=RPORT):
        self.redisdbnum = dbnum
        self.conn = redis.StrictRedis(host=host, port=port, decode_responses=True,
                                      db=self.redisdbnum, socket_connect_timeout=5)
        super().__init__()

    def delete_table(self):
        """
        deletes table from db\n
        :return:
        """
        self.flush()

    def create_table(self):
        """
        creates a new table, delete first if exists \n
        :return:
        """

    def dbsize(self) -> int:
        """
        returns the itemcount in db\n
        :return: item count
        """
        return len(self.keys())

    def keys(self, pattern='*') -> List[str]:
        """
        returns keys list in db \n
        :param pattern: str urlpathregex
        :return: the keys in db
        """
        return list(
            set(self.conn.keys(pattern=pattern)) - set(self.conn.keys(self.tagprefix + "*")))

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        get value by key\n
        :param key: str
        :return: dict or None
        """
        if not isinstance(key, str):
            raise TypeError("key must be str, got " + str(type(key)))
        retval = None
        resp = self.conn.get(key)

        if resp:
            resp = json.loads(resp)
            if not isinstance(resp, dict):
                retval = {key: resp}
            else:
                retval = resp

        return retval

    def get_multi(self, keylist: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        get value by key\n
        :param keylist: list of strings
        :return: [objectdict]
        """
        retdict: Dict[str, Any] = {}
        retlist = self.conn.mget(keylist)

        for i, rstr in enumerate(retlist):
            # noinspection PyBroadException
            try:
                retdict[keylist[i]] = json.loads(rstr)
            except Exception:  # pylint: disable=broad-except
                retdict[keylist[i]] = str(rstr)
        return retdict

    def get_all_as_list(self) -> List[Optional[Dict[str, Any]]]:
        """
        get all values in store \n
        :return: list
        """
        keys = self.keys()
        retlist = []
        for key in keys:
            retlist.append(self.get(key))

        return retlist

    def get_all_as_dict(self) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        get all values in store \n
        :return: dict
        """
        keys = self.keys()
        retdct = {}
        for key in keys:
            retdct[key] = self.get(key)

        return retdct

    def upsert(self, key: str, value: Dict[str, Any]) -> bool:
        """
        get all values in store \n
        :return: list
        """
        key = str(key)
        if not isinstance(value, dict):
            raise TypeError("value must be dict but got" + str(type(value)))
        nvalue = json.dumps(value, ensure_ascii=False)
        return bool(self.conn.set(key, nvalue))

    def upsert_multi(self, itemdict: Dict[str, Dict[str, Any]]):
        """
        upsert multiple items at once\n
        :param itemdict: dict of objects dictionaries
        :return: bool
        """
        pipe = self.conn.pipeline()
        for key, item in itemdict.items():
            mvalue = item.copy()
            if "idkey" not in mvalue or not mvalue["idkey"]:
                mvalue["idkey"] = str(key)
            nvalue = json.dumps(mvalue, ensure_ascii=False)
            pipe.set(str(key), nvalue)
        pipe.execute()

    def remove(self, key: str) -> bool:
        """
        removes the key from store\n
        :param key: str or list or tuple
        :return:
        """
        key = str(key)
        ret = str(self.conn.delete(key))
        return {"1": True}.get(ret, False)

    def remove_keys(self, keys: List[str]) -> bool:
        """
        removes the key from store\n
        :param keys:
        :return:
        """
        for key in keys:
            self.conn.delete(key)
        return True

    def flush(self):
        """
        Flushes current store\n
        :return: None
        """
        self.conn.flushdb()

    def tags(self) -> List[str]:
        """
        returns tag list \n
        :return:
        """
        taglist = self.conn.keys(self.tagprefix + "*")
        retlist = []
        for tag in taglist:
            retlist.append(tag.replace(self.tagprefix, ""))
        return retlist

    def gettagkeys(self, tag: str) -> List[str]:
        """
        get all keys of given tag \n
        :param tag:
        :return:
        """
        memberids = self.conn.smembers(self.tagprefix + tag)
        return list(memberids)

    def gettag(self, tag: str) -> List[Optional[Dict[str, Any]]]:
        """
        get all dict items in given tag \n
        :param tag:
        :return: list of dictionaries
        """
        memberids = self.gettagkeys(tag)
        retlist = []
        for memberid in list(memberids):
            retlist.append(self.get(memberid))

        return retlist

    def addtag(self, tag: str, key: str):
        """
        Adds tags to keys \n
        :param tag: list
        :param key: list
        :return: None
        """
        if not (tag and key):
            raise ValueError
        self.conn.sadd(self.tagprefix + tag, key)

    def removefromtag(self, tag: str, key: Union[str, list]):
        """
        Remove items from lists \n
        :param tag: str
        :param key: str or list
        :return: None
        """
        tag = str(tag)
        # ! dont touch it. srem doesnt accept list !!!!!
        if isinstance(key, (list, tuple, set)):
            for k in key:
                self.conn.srem(self.tagprefix + tag, k)
        else:
            self.conn.srem(self.tagprefix + tag, key)
