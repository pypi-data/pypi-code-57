'''_1151.py

SplineFixtureTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPLINE_FIXTURE_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'SplineFixtureTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('SplineFixtureTypes',)


class SplineFixtureTypes(Enum):
    '''SplineFixtureTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SPLINE_FIXTURE_TYPES
    __hash__ = None

    FLEXIBLE = 0
    FIXED = 1
