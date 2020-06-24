'''_1156.py

SplineToleranceClassTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPLINE_TOLERANCE_CLASS_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'SplineToleranceClassTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('SplineToleranceClassTypes',)


class SplineToleranceClassTypes(Enum):
    '''SplineToleranceClassTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SPLINE_TOLERANCE_CLASS_TYPES
    __hash__ = None

    _4 = 0
    _5 = 1
    _6 = 2
    _7 = 3
    _8 = 4
    _9 = 5
    _10 = 6
    _11 = 7
    _12 = 8
