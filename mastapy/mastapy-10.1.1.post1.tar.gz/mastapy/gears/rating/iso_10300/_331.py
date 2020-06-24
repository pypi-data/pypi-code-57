'''_331.py

ISO10300RatingMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ISO10300_RATING_METHOD = python_net_import('SMT.MastaAPI.Gears.Rating.Iso10300', 'ISO10300RatingMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO10300RatingMethod',)


class ISO10300RatingMethod(Enum):
    '''ISO10300RatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ISO10300_RATING_METHOD
    __hash__ = None

    METHOD_B1 = 0
    METHOD_B2 = 1
