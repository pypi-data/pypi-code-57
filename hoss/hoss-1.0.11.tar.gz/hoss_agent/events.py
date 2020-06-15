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


import random

from hoss_agent.utils.encoding import keyword_field
from hoss_agent.utils.logging import get_logger

__all__ = ("BaseEvent", "Exception", "Message")

logger = get_logger("hoss_agent.events")


class BaseEvent(object):
    @staticmethod
    def to_string(client, data):
        raise NotImplementedError

    @staticmethod
    def capture(client, **kwargs):
        return {}


class Exception(BaseEvent):
    """
    Exceptions store the following metadata:

    - value: 'My exception value'
    - type: 'ClassName'
    - module '__builtin__' (i.e. __builtin__.TypeError)
    - frames: a list of serialized frames (see _get_traceback_frames)
    """

    @staticmethod
    def to_string(client, data):
        exc = data["exception"]
        if exc["value"]:
            return "%s: %s" % (exc["type"], exc["value"])
        return exc["type"]

    @staticmethod
    def get_hash(data):
        exc = data["exception"]
        output = [exc["type"]]
        for frame in data["stacktrace"]["frames"]:
            output.append(frame["module"])
            output.append(frame["function"])
        return output


class Message(BaseEvent):
    """
    Messages store the following metadata:

    - message: 'My message from %s about %s'
    - params: ('foo', 'bar')
    """

    @staticmethod
    def to_string(client, data):
        return data["log"]["message"]

    @staticmethod
    def get_hash(data):
        msg = data["param_message"]
        return [msg["message"]]

    @staticmethod
    def capture(client, param_message=None, message=None, level=None, logger_name=None, **kwargs):
        if message:
            param_message = {"message": message}
        params = param_message.get("params")
        message = param_message["message"] % params if params else param_message["message"]
        data = kwargs.get("data", {})
        message_data = {
            "id": "%032x" % random.getrandbits(128),
            "log": {
                "level": keyword_field(level or "error"),
                "logger_name": keyword_field(logger_name or "__root__"),
                "message": message,
                "param_message": keyword_field(param_message["message"]),
            },
        }
        if isinstance(data.get("stacktrace"), dict):
            message_data["log"]["stacktrace"] = data["stacktrace"]["frames"]
        if kwargs.get("exception"):
            message_data["culprit"] = kwargs["exception"]["culprit"]
            message_data["exception"] = kwargs["exception"]["exception"]
        return message_data
