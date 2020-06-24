'''_845.py

ShaperEdgeTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SHAPER_EDGE_TYPES = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'ShaperEdgeTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaperEdgeTypes',)


class ShaperEdgeTypes(Enum):
    '''ShaperEdgeTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SHAPER_EDGE_TYPES
    __hash__ = None

    SINGLE_CIRCLE = 0
    CATMULLROM_SPLINE = 1
