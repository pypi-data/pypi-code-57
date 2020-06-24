'''_1490.py

BearingToleranceDefinitionOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_TOLERANCE_DEFINITION_OPTIONS = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'BearingToleranceDefinitionOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingToleranceDefinitionOptions',)


class BearingToleranceDefinitionOptions(Enum):
    '''BearingToleranceDefinitionOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_TOLERANCE_DEFINITION_OPTIONS
    __hash__ = None

    CLASSES = 0
    VALUES = 1
