'''_609.py

ManufactureRating
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MANUFACTURE_RATING = python_net_import('SMT.MastaAPI.Gears.Materials', 'ManufactureRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ManufactureRating',)


class ManufactureRating(Enum):
    '''ManufactureRating

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MANUFACTURE_RATING
    __hash__ = None

    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
