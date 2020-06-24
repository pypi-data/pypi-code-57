'''_1092.py

GleasonSafetyRequirements
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_GLEASON_SAFETY_REQUIREMENTS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'GleasonSafetyRequirements')


__docformat__ = 'restructuredtext en'
__all__ = ('GleasonSafetyRequirements',)


class GleasonSafetyRequirements(Enum):
    '''GleasonSafetyRequirements

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _GLEASON_SAFETY_REQUIREMENTS
    __hash__ = None

    MAXIMUM_SAFETY = 0
    FEWER_THAN_1_FAILURE_IN_100 = 1
    FEWER_THAN_1_FAILURE_IN_3 = 2
