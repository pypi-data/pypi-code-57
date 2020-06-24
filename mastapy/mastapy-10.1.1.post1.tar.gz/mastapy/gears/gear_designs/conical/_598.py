'''_598.py

LoadDistributionFactorMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LOAD_DISTRIBUTION_FACTOR_METHODS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'LoadDistributionFactorMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadDistributionFactorMethods',)


class LoadDistributionFactorMethods(Enum):
    '''LoadDistributionFactorMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _LOAD_DISTRIBUTION_FACTOR_METHODS
    __hash__ = None

    CALCULATE_FROM_MISALIGNMENT = 0
    DETERMINED_FROM_APPLICATION_AND_MOUNTING = 1
    SPECIFIED = 2
