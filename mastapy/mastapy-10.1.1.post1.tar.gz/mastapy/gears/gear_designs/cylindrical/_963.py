'''_963.py

AddendumModificationDistributionRule
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ADDENDUM_MODIFICATION_DISTRIBUTION_RULE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'AddendumModificationDistributionRule')


__docformat__ = 'restructuredtext en'
__all__ = ('AddendumModificationDistributionRule',)


class AddendumModificationDistributionRule(Enum):
    '''AddendumModificationDistributionRule

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ADDENDUM_MODIFICATION_DISTRIBUTION_RULE
    __hash__ = None

    USERSPECIFIED = 0
    ZERO_PINION_PROFILE_SHIFT_COEFFICIENT = 1
    GENERAL_APPLICATIONS = 2
    EQUAL_BENDING_STRENGTH = 3
    BALANCE_SLIDE_ROLL_RATIOS = 4
    INCREASING_SPEED = 5
    AVOID_UNDERCUT = 6
