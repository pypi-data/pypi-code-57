#  BSD 3-Clause License
#
#  Copyright (c) 2012, the Sentry Team, see AUTHORS for more details
#  Copyright (c) 2019, Elasticsearch BV
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
import sys

__all__ = ("VERSION", "Client")

try:
    VERSION = __import__("pkg_resources").get_distribution("hoss").version
except Exception:
    VERSION = "unknown"

from hoss_agent.base import Client
from hoss_agent.instrumentation.control import instrument
from hoss_agent.utils.logging import get_logger

GLOBAL_CLIENT = None
logger = get_logger("hoss_agent")


def init(config=None, *args, **inline):

    if isinstance(config, str):
        if len(config) == 0:
            logger.info('Hoss API Key is not provided. Exiting')
            return
        if len(args) >= 1 and isinstance(args[0], dict):
            args[0]['API_KEY'] = config
            client = Client(args[0], **inline)
        else:
            client = Client({"API_KEY": config}, **inline)
    else:
        if not config or not config['API_KEY']:
            logger.info('Hoss API Key is not provided. Exiting')
            return
        client = Client(config, **inline)

    client.instrument()
    client.start_threads()
    global GLOBAL_CLIENT
    GLOBAL_CLIENT = client
    return client
