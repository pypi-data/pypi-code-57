'''_255.py

LubricantViscosityClassAGMA
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LUBRICANT_VISCOSITY_CLASS_AGMA = python_net_import('SMT.MastaAPI.Materials', 'LubricantViscosityClassAGMA')


__docformat__ = 'restructuredtext en'
__all__ = ('LubricantViscosityClassAGMA',)


class LubricantViscosityClassAGMA(Enum):
    '''LubricantViscosityClassAGMA

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _LUBRICANT_VISCOSITY_CLASS_AGMA
    __hash__ = None

    AGMA_1 = 46
    AGMA_2 = 68
    AGMA_3 = 100
    AGMA_4 = 150
    AGMA_5 = 220
    AGMA_6 = 320
    AGMA_7 = 460
    AGMA_8 = 680
    AGMA_8A = 1000
