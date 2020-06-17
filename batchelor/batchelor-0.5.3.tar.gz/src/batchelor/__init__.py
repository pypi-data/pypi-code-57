__version__ = '0.5.3'
_start_ = 1
from .main import (
    __checkpoint__, __write__, __visual__, __save_name__,
    fast, medium, default, slow,
    Batch, prompt, launch
)
_end_ = 1


def __generate__():
    add = False
    value = {}
    for k in globals():
        if add:
            if k == '_end_':
                break
            value[k] = globals()[k]
        elif k == '_start_':
            add = True
    return value

__all__ = __generate__()
del _start_, _end_, __generate__
