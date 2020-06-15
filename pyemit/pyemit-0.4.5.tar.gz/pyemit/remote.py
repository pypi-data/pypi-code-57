#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Aaron-Yang [code@jieyu.ai]
Contributors:

"""
import json
import logging
import pickle
import uuid
from typing import Any

from pyemit.emit import rpc_send, rpc_respond

logger = logging.getLogger(__name__)


class Remote(object):
    _proto_ = 4

    def __init__(self, timeout=10):
        self._sn_ = uuid.uuid4().hex
        self._ver_ = '0.1'
        self._timeout_ = timeout

    def __str__(self):
        def default(obj):
            return obj.__str__()

        return json.dumps(self.__dict__, default=default, indent=2)

    def __repr__(self):
        return f"{self.__class__} 0x{id(self):0x}\n{self.__str__()}"

    @property
    def sn(self):
        return self._sn_

    @property
    def timeout(self):
        return self._timeout_

    @staticmethod
    def loads(s) -> 'Remote':
        return pickle.loads(s)

    async def invoke(self):
        return await rpc_send(self)

    async def server_impl(self):
        raise NotImplementedError

    async def respond(self, result: Any):
        response = {
            '_sn_':   self._sn_,
            '_data_': pickle.dumps(result, protocol=Remote._proto_)
        }

        await rpc_respond(response)
