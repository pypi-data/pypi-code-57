'''_127.py

DeflectionFromBendingOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DEFLECTION_FROM_BENDING_OPTION = python_net_import('SMT.MastaAPI.Gears', 'DeflectionFromBendingOption')


__docformat__ = 'restructuredtext en'
__all__ = ('DeflectionFromBendingOption',)


class DeflectionFromBendingOption(Enum):
    '''DeflectionFromBendingOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _DEFLECTION_FROM_BENDING_OPTION

    __hash__ = None

    ACCURATE_CALCULATION = 0
    BASIC_TOTAL_SINGLE_TOOTH_STIFFNESS_IS_14_NUM_MM_AS_SUGGESTED_BY_ISO = 1
    ESTIMATED_FROM_FE_MODEL = 2
    NONE = 3
