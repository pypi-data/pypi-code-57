'''_6179.py

SystemOptimiserGearSetOptimisation
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SYSTEM_OPTIMISER_GEAR_SET_OPTIMISATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'SystemOptimiserGearSetOptimisation')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemOptimiserGearSetOptimisation',)


class SystemOptimiserGearSetOptimisation(Enum):
    '''SystemOptimiserGearSetOptimisation

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SYSTEM_OPTIMISER_GEAR_SET_OPTIMISATION
    __hash__ = None

    NONE = 0
    FAST = 1
    FULL = 2
