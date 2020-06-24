'''_1030.py

StressRegions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_STRESS_REGIONS = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.InterferenceFits', 'StressRegions')


__docformat__ = 'restructuredtext en'
__all__ = ('StressRegions',)


class StressRegions(Enum):
    '''StressRegions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _STRESS_REGIONS

    __hash__ = None

    FULLY_ELASTIC = 0
    PLASTICELASTIC = 1
    FULLY_PLASTIC = 2
