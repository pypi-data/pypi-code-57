'''_1062.py

ComplexPartDisplayOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_COMPLEX_PART_DISPLAY_OPTION = python_net_import('SMT.MastaAPI.MathUtility', 'ComplexPartDisplayOption')


__docformat__ = 'restructuredtext en'
__all__ = ('ComplexPartDisplayOption',)


class ComplexPartDisplayOption(Enum):
    '''ComplexPartDisplayOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _COMPLEX_PART_DISPLAY_OPTION

    __hash__ = None

    MODULUS = 0
    PHASE = 1
    REAL = 2
    IMAGINARY = 3
