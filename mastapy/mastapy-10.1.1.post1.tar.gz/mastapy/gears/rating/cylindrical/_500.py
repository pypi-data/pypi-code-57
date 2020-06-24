'''_500.py

RatingMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RATING_METHOD = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'RatingMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('RatingMethod',)


class RatingMethod(Enum):
    '''RatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _RATING_METHOD
    __hash__ = None

    METHOD_B = 0
    METHOD_C = 1
