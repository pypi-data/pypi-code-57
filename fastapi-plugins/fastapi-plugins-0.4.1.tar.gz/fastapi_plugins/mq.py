#!/usr/bin/env python
# -*- coding: utf-8 -*-
# fastapi_plugins.mq
'''
:author:    madkote
:contact:   madkote(at)bluewin.ch
:copyright: Copyright 2020, madkote

fastapi_plugins.mq
------------------
Messaging queue
'''

from __future__ import absolute_import

import aio_pika
import starlette.requests

from .plugin import PluginSettings
from .plugin import Plugin
from .version import VERSION

__all__ = []
__author__ = 'madkote <madkote(at)bluewin.ch>'
__version__ = '.'.join(str(x) for x in VERSION)
__copyright__ = 'Copyright 2020, madkote'


# =============================================================================
# PIKA
# =============================================================================
#
# TODO: xxx
# * connection pool
# * channel pool
#
# =============================================================================
class PikaManager():
    pass


class PikaSettings(PluginSettings):
    pass


class PikaPlugin(Plugin):
    DEFAULT_CONFIG_CLASS = PikaSettings


pika_plugin = PikaPlugin()


async def depends_pika(
    request: starlette.requests.Request
) -> aio_pika.Channel:
    return await request.app.state.AIOPIKA()


async def depends_pika_connection(
    request: starlette.requests.Request
) -> aio_pika.Connection:
    return await request.app.state.AIOPIKA.get_connection()


# =============================================================================
# TODO: xxx
# =============================================================================
# class MQ():
#     async def publish(self, topic, message, headers=None):
#         raise NotImplementedError
#
#
# class MQSettings(PluginSettings):
#     pass
#
#
# class MQPlugin(Plugin):
#     DEFAULT_CONFIG_CLASS = MQSettings
#
#
# mq_plugin = MQPlugin()
#
#
# async def depends_mq(
#     request: starlette.requests.Request
# ) -> MQ:
#     return await request.app.state.MQ()
