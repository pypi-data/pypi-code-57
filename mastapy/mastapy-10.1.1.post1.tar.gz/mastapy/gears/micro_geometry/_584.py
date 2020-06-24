'''_584.py

ParabolicTipReliefStartsTangentToMainProfileRelief
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PARABOLIC_TIP_RELIEF_STARTS_TANGENT_TO_MAIN_PROFILE_RELIEF = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'ParabolicTipReliefStartsTangentToMainProfileRelief')


__docformat__ = 'restructuredtext en'
__all__ = ('ParabolicTipReliefStartsTangentToMainProfileRelief',)


class ParabolicTipReliefStartsTangentToMainProfileRelief(Enum):
    '''ParabolicTipReliefStartsTangentToMainProfileRelief

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _PARABOLIC_TIP_RELIEF_STARTS_TANGENT_TO_MAIN_PROFILE_RELIEF
    __hash__ = None

    NO = 0
    YES = 1
    ONLY_WHEN_NONZERO_PARABOLIC_TIP_RELIEF = 2
