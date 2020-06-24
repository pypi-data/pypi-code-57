'''_1000.py

SplineRatingTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPLINE_RATING_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'SplineRatingTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('SplineRatingTypes',)


class SplineRatingTypes(Enum):
    '''SplineRatingTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _SPLINE_RATING_TYPES

    __hash__ = None

    GBT_178551999 = 0
    SAE_B9211996 = 1
    DIN_5466 = 2
    AGMA_6123C16 = 3
