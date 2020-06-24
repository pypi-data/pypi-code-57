'''_83.py

RatingTypeForBearingReliability
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RATING_TYPE_FOR_BEARING_RELIABILITY = python_net_import('SMT.MastaAPI.NodalAnalysis', 'RatingTypeForBearingReliability')


__docformat__ = 'restructuredtext en'
__all__ = ('RatingTypeForBearingReliability',)


class RatingTypeForBearingReliability(Enum):
    '''RatingTypeForBearingReliability

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _RATING_TYPE_FOR_BEARING_RELIABILITY
    __hash__ = None

    ISO_2812007 = 0
    ISO_2812007_WITH_LIFE_MODIFICATION_FACTOR = 1
    ISOTS_162812008 = 2
    ISOTS_162812008_WITH_LIFE_MODIFICATION_FACTOR = 3
