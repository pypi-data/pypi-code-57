#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
from functools import update_wrapper
from threading import RLock


class lazy_property:
    """A decorator that converts a function into a lazy property with thread locking"""

    def __init__(self, func):
        self.lock = RLock()
        self.func = func
        update_wrapper(self, func)

    def __call__(self, instance, cls):
        return self.__get__(instance, cls)

    def __get__(self, instance, cls):
        with self.lock:
            if self.func not in instance.__dict__:
                instance.__dict__[self.func] = self.func(instance)
        return instance.__dict__[self.func]
