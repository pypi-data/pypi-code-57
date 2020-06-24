'''_1209.py

ThreadTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_THREAD_TYPES = python_net_import('SMT.MastaAPI.Bolts', 'ThreadTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('ThreadTypes',)


class ThreadTypes(Enum):
    '''ThreadTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _THREAD_TYPES
    __hash__ = None

    METRIC_STANDARD_THREAD = 0
    METRIC_FINE_THREAD = 1
