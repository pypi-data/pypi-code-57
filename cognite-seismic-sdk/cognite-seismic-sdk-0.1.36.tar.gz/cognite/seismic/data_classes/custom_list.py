# Copyright 2019 Cognite AS

import inspect


class CustomList(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return iter(self.iterable)

    def to_list(self):
        self.load()
        return self.iterable

    def load(self):
        if not isinstance(self.iterable, list):
            self.iterable = list(self.iterable)
