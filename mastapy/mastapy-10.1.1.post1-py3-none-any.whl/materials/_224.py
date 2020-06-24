'''_224.py

AcousticRadiationEfficiencyInputType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ACOUSTIC_RADIATION_EFFICIENCY_INPUT_TYPE = python_net_import('SMT.MastaAPI.Materials', 'AcousticRadiationEfficiencyInputType')


__docformat__ = 'restructuredtext en'
__all__ = ('AcousticRadiationEfficiencyInputType',)


class AcousticRadiationEfficiencyInputType(Enum):
    '''AcousticRadiationEfficiencyInputType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ACOUSTIC_RADIATION_EFFICIENCY_INPUT_TYPE
    __hash__ = None

    SPECIFY_VALUES = 0
    SIMPLE_PARAMETRISED = 1
    UNITY = 2
