from typing import TypeVar

StreamType = TypeVar('StreamType')
JoinedStreamType = TypeVar('JoinedStreamType')
ResultStreamType = TypeVar('ResultStreamType')


class AliasType:
    def __init__(self, origin_cls, alias):
        self.origin_cls = origin_cls
        self.alias = alias
        self.__name__ = alias

    def __hash__(self):
        return hash(self.alias)

    def __eq__(self, other):
        return self.alias == other.alias

    def __call__(self, *args, **kwargs):
        return self.origin_cls(*args, **kwargs)


def type_alias(stream_type, alias: str):
    return AliasType(stream_type, alias)
