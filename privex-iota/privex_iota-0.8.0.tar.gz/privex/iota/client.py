"""
Copyright::

    +===================================================+
    |                 © 2020 Privex Inc.                |
    |               https://www.privex.io               |
    +===================================================+
    |                                                   |
    |        Privex's Random IOTA Tools                 |
    |        License: X11/MIT                           |
    |                                                   |
    |        Core Developer(s):                         |
    |                                                   |
    |          (+)  Chris (@someguy123) [Privex]        |
    |                                                   |
    +===================================================+

    Privex's Random IOTA Tools
    Copyright (c) 2020    Privex Inc. ( https://www.privex.io )

"""
import sys

from iota import Iota
from privex.helpers import DictObject, empty_if, empty

from privex.iota import objects, settings

__all__ = [
    'PrivexIota', 'err', 'get_iota'
]


def err(*args, file=sys.stderr, **kwargs):
    print(*args, file=file, **kwargs)


STORAGE = DictObject(iota=None)


def get_iota(host=None, new_instance=False, **kwargs) -> "PrivexIota":
    host = empty_if(host, settings.IOTA_HOST)
    if new_instance or empty(STORAGE.get('iota')):
        if 'iota' in STORAGE:
            del STORAGE['iota']
        STORAGE.iota = PrivexIota(adapter=host, **kwargs)
    return STORAGE.iota


class PrivexIota(Iota):
    def get_node_info(self) -> objects.NodeInfo:
        info = super(PrivexIota, self).get_node_info()
        return objects.NodeInfo.from_dict(info)
    
    def get_neighbors(self) -> objects.NeighborRes:
        neighbors = super(PrivexIota, self).get_neighbors()
        return objects.NeighborRes.from_dict(neighbors)


