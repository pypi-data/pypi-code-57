'''_256.py

LubricantViscosityClassification
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LUBRICANT_VISCOSITY_CLASSIFICATION = python_net_import('SMT.MastaAPI.Materials', 'LubricantViscosityClassification')


__docformat__ = 'restructuredtext en'
__all__ = ('LubricantViscosityClassification',)


class LubricantViscosityClassification(Enum):
    '''LubricantViscosityClassification

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _LUBRICANT_VISCOSITY_CLASSIFICATION
    __hash__ = None

    ISO = 0
    AGMA = 1
    SAE = 2
    USERSPECIFIED = 3
