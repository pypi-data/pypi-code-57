# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import time


class ConnectionStatus(object):
    """
    Stores the connection information between the agent and the service
    """

    def __init__(self):
        self._connected = False
        self.connection_attempts = 0
        self.last_attempt = None

        self._success = 0
        self._failed = 0

    @property
    def failure_count(self):
        return self._failed

    @property
    def success_count(self):
        return self._success

    @property
    def connected(self):
        return self._connected

    @property
    def was_connected(self):
        return self._success > 0

    def success(self):
        self._connected = True
        self.last_attempt = None
        self._success += 1
        self.connection_attempts = 0

    def failure(self):
        self._connected = False
        self.last_attempt = int(time.time() * 1000)
        self._failed += 1
        self.connection_attempts += 1
