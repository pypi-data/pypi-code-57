'''_1144.py

SAEFatigueLifeFactorTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SAE_FATIGUE_LIFE_FACTOR_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'SAEFatigueLifeFactorTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('SAEFatigueLifeFactorTypes',)


class SAEFatigueLifeFactorTypes(Enum):
    '''SAEFatigueLifeFactorTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SAE_FATIGUE_LIFE_FACTOR_TYPES
    __hash__ = None

    UNIDIRECTIONAL = 0
    FULLY_REVERSED = 1
