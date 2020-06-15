# -*- coding: utf-8 -*-

import json

class FrozenDict(dict):
    """A cheap and cheerful immutable dictionary.

    This class behaves exactly like a normal python dictionary except
    for two features

    * Once created, elements of the dictionary can not be added or changed.
      This makes the object immutable
    * Because it is immutable, we can implement a hashing function, and
      use a FrozenDict as a key in another dictionary.

    The FrozenDict is not completely immutable. It doesn't stop you from
    creating an instance with a mutable value inside (e.g `FrozenDict(a=list(...))`.
    Such an object will behave normally until such time as you try to
    find its hash (e.g when using it as a dictionary key), at which point
    it will raise an Exception.

    For our purpose, we know this won't happen in the intended use case,
    and don't spend time checking for this fail case.
    """

    def __setitem__(self, k, v):
        raise TypeError("Properties of FrozenDict are immutable")

    def __repr__(self):
        return "F" + dict.__repr__(self)

    def __hash__(self):
        """This hashing algorithm from Stack overflow
        https://stackoverflow.com/a/2704866/46407
        """

        hash_ = 0
        for pair in self.items():
            hash_ ^= hash(pair)
        self._hash = hash_
        return self._hash

    def setdefault(self, k, v):
        """You would expect this to call setitem, but it doesn't"""
        raise TypeError("Properties of FrozenDict are immutable")

    def update(self, *args, **kwargs):
        raise TypeError("Properties of FrozenDict are immutable")


class FrozenDictEncoder(json.JSONEncoder):
    """Teach json how to encode a FrozenDict"""
    def default(self, obj):
        if isinstance(obj, FrozenDict):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)
