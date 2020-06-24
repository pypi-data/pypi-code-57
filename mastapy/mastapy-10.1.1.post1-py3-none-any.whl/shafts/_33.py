'''_33.py

ShaftRatingMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SHAFT_RATING_METHOD = python_net_import('SMT.MastaAPI.Shafts', 'ShaftRatingMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftRatingMethod',)


class ShaftRatingMethod(Enum):
    '''ShaftRatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _SHAFT_RATING_METHOD

    __hash__ = None

    DIN_743201212 = 0
    SMT = 1
    AGMA_60016101E08 = 2
    FKM_GUIDELINE_6TH_EDITION_2012 = 3
