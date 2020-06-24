'''_251.py

ISO76StaticSafetyFactorLimits
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ISO76_STATIC_SAFETY_FACTOR_LIMITS = python_net_import('SMT.MastaAPI.Materials', 'ISO76StaticSafetyFactorLimits')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO76StaticSafetyFactorLimits',)


class ISO76StaticSafetyFactorLimits(Enum):
    '''ISO76StaticSafetyFactorLimits

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ISO76_STATIC_SAFETY_FACTOR_LIMITS
    __hash__ = None

    QUIETRUNNING_APPLICATIONS_SMOOTHRUNNING_VIBRATIONFREE_HIGH_ROTATIONAL_ACCURACY = 0
    NORMALRUNNING_APPLICATIONS_SMOOTHRUNNING_VIBRATIONFREE_NORMAL_ROTATIONAL_ACCURACY = 1
    APPLICATIONS_SUBJECTED_TO_SHOCK_LOADS_PRONOUNCED_SHOCK_LOADS = 2
