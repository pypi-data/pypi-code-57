# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import division
import time


class Timer(object):
    """
    Utility class to store timing by a key

    Example:
        t = Timer()

        set_start('bob')
        something()
        set_end('body')

    """

    def __init__(self, start_time=None):
        if start_time is None:
            start_time = time.time()

        self.start_at = start_time
        self.start_ms = int(self.start_at * 1000)
        self.events = dict()

        self.result = None

    def set_start(self, name):
        self.events[name] = [Timer.now_ms(), None]

    def set_end(self, name):
        self.events[name][1] = Timer.now_ms()

    @staticmethod
    def now_ms():
        return int(time.time() * 1000)
