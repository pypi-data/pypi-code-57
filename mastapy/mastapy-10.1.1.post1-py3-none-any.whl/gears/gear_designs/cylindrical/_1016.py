'''_1016.py

TipAlterationCoefficientMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TIP_ALTERATION_COEFFICIENT_METHOD = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'TipAlterationCoefficientMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('TipAlterationCoefficientMethod',)


class TipAlterationCoefficientMethod(Enum):
    '''TipAlterationCoefficientMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TIP_ALTERATION_COEFFICIENT_METHOD
    __hash__ = None

    USERSPECIFIED = 0
    B = 1
    C = 2
