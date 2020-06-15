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


from __future__ import absolute_import

import itertools
import os
import platform
import threading

import hoss_agent
from hoss_agent.conf import Config, VersionedConfig, constants
from hoss_agent.conf.constants import ERROR
from hoss_agent.utils import compat, is_master_process
from hoss_agent.utils.logging import get_logger
from hoss_agent.utils.module_import import import_string
from hoss_agent.context import execution_context

__all__ = ("Client",)


class Client(object):
    """
    The base hoss_agent client, which handles communication over the
    HTTP API to the ingress service.
    """

    logger = get_logger("hoss_agent")

    def __init__(self, config=None, **inline):
        # configure loggers first
        cls = self.__class__
        self.logger = get_logger("%s.%s" % (cls.__module__, cls.__name__))
        self.error_logger = get_logger("hoss_agent.errors")

        self._pid = None
        self._thread_starter_lock = threading.Lock()
        self._thread_managers = {}

        self.tracer = None
        self.processors = []
        self.filter_exception_types_dict = {}
        self._service_info = None

        config = Config(config, inline_dict=inline)
        if config.errors:
            for msg in config.errors.values():
                self.error_logger.error(msg)
            config.disable_send = True
        self.config = VersionedConfig(config, version=None)
        headers = {
            "Content-Type": "application/json",
            "Content-Encoding": "gzip",
            "User-Agent": "hoss_agent-python/%s" % hoss_agent.VERSION,
        }

        transport_kwargs = {
            "headers": headers,
            "verify_server_cert": self.config.verify_server_cert,
            "server_cert": self.config.server_cert,
            "timeout": self.config.server_timeout,
            "max_flush_time": self.config.api_request_time / 1000.0,
            "max_buffer_size": self.config.api_request_size,
            "processors": self.load_processors(),
        }
        self._api_endpoint_url = compat.urlparse.urljoin(
            self.config.server_url if self.config.server_url.endswith("/") else self.config.server_url + "/",
            constants.EVENTS_API_PATH,
        )
        self._config_endpoint_url = compat.urlparse.urljoin(
            self.config.config_server_url if self.config.config_server_url.endswith("/") else self.config.config_server_url + "/",
            constants.AGENT_CONFIG_PATH,
        )
        transport_class = import_string(self.config.transport_class)
        self._transport = transport_class(self._api_endpoint_url, self, **transport_kwargs)
        self.config.transport = transport_class(self._config_endpoint_url, self, **transport_kwargs)
        self._thread_managers["transport"] = self._transport

        if platform.python_implementation() == "PyPy":
            # PyPy introduces a `_functools.partial.__call__` frame due to our use
            # of `partial` in AbstractInstrumentedModule
            skip_modules = ("hoss_agent.", "_functools")
        else:
            skip_modules = ("hoss_agent.",)

        compat.atexit_register(self.close)
        if self.config.central_config:
            self._thread_managers["config"] = self.config
        else:
            self._config_updater = None

        execution_context.set_events([])
        execution_context.set_client(self)

    def start_threads(self):
        with self._thread_starter_lock:
            current_pid = os.getpid()
            if self._pid != current_pid:
                self.logger.debug("Detected PID change from %s to %d, starting threads", self._pid, current_pid)
                for manager_type, manager in self._thread_managers.items():
                    self.logger.debug("Starting %s thread", manager_type)
                    manager.start_thread()
                self._pid = current_pid

    def get_handler(self, name):
        return import_string(name)

    def capture(self, event_type, date=None, context=None, custom=None, stack=None, handled=True, **kwargs):
        """
        Captures and processes an event and pipes it off to Client.send.
        """
        if event_type == "Exception":
            # never gather log stack for exceptions
            stack = False
        data = self._build_msg_for_logging(
            event_type, date=date, context=context, custom=custom, stack=stack, handled=handled, **kwargs
        )

        if data:
            # queue data, and flush the queue if this is an unhandled exception
            self.queue(ERROR, data, flush=not handled)
            return data["id"]

    def capture_message(self, message=None, param_message=None, **kwargs):
        """
        Creates an event from ``message``.

        >>> client.capture_message('My event just happened!')
        """
        return self.capture("Message", message=message, param_message=param_message, **kwargs)

    def should_queue(self, data):
        for black_list_host in self.config.account_api_configuration['host_black_list']:
            if black_list_host in data['request']['url']:
                return False
        if self.config.disable_send:
            return False
        return True

    def flush(self):
        self._transport.flush()

    def queue(self, event_type, data, flush=False):
        if not self.should_queue(data):
            return
        self.start_threads()
        if flush and is_master_process():
            # don't flush in uWSGI master process to avoid ending up in an unpredictable threading state
            flush = False
        self._transport.queue(event_type, data, flush)

    def close(self):
        with self._thread_starter_lock:
            for _manager_type, manager in self._thread_managers.items():
                manager.stop_thread()

    def instrument(self):
        hoss_agent.instrument()

    def instrument(self):
        hoss_agent.instrument()

    def load_processors(self):
        """
        Loads processors from self.config.processors, as well as constants.HARDCODED_PROCESSORS.
        Duplicate processors (based on the path) will be discarded.

        :return: a list of callables
        """
        processors = itertools.chain(self.config.processors, constants.HARDCODED_PROCESSORS)
        seen = {}
        # setdefault has the nice property that it returns the value that it just set on the dict
        return [seen.setdefault(path, import_string(path)) for path in processors if path not in seen]


class DummyClient(Client):
    """Sends messages into an empty void"""

    def send(self, url, **kwargs):
        return None
