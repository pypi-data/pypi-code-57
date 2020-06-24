'''_1148.py

SplineDesignTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPLINE_DESIGN_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'SplineDesignTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('SplineDesignTypes',)


class SplineDesignTypes(Enum):
    '''SplineDesignTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SPLINE_DESIGN_TYPES
    __hash__ = None

    DIN_548012006 = 0
    ISO_4156122005 = 1
    GBT_347812008 = 2
    JIS_B_16032001 = 3
    SAE_B9211996 = 4
    CUSTOM = 5
