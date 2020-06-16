# coding=utf-8
from __future__ import absolute_import, print_function

import abc
import time

from suanpan import objects


class Loop(objects.HasName):
    __metaclass__ = abc.ABCMeta

    def __call__(self):
        return self.loop()

    @abc.abstractmethod
    def loop(self):
        pass


class Interval(Loop):
    def __init__(self, seconds, pre=False):
        self.seconds = seconds
        self.pre = pre

    def loop(self):
        while True:
            if self.pre:
                time.sleep(self.seconds)
            yield
            if not self.pre:
                time.sleep(self.seconds)


class IntervalIndex(Interval):
    def loop(self):
        for i, _ in enumerate(super(IntervalIndex, self).loop()):
            yield i
