'''_277.py

EfficiencyRatingMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_EFFICIENCY_RATING_METHOD = python_net_import('SMT.MastaAPI.Materials.Efficiency', 'EfficiencyRatingMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('EfficiencyRatingMethod',)


class EfficiencyRatingMethod(Enum):
    '''EfficiencyRatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _EFFICIENCY_RATING_METHOD
    __hash__ = None

    ISOTR_1417912001 = 0
    ISOTR_1417922001 = 1
