'''_923.py

ToothProportionsInputMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TOOTH_PROPORTIONS_INPUT_METHOD = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'ToothProportionsInputMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('ToothProportionsInputMethod',)


class ToothProportionsInputMethod(Enum):
    '''ToothProportionsInputMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _TOOTH_PROPORTIONS_INPUT_METHOD

    __hash__ = None

    DIRECT_DIMENSIONAL_INPUT = 0
    ADDENDUMDEPTH_FACTORS = 1
    GLEASON_FACTORS_OLD = 2
