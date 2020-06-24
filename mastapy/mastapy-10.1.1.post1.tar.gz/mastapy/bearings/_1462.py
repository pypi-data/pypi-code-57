'''_1462.py

BearingCageMaterial
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_CAGE_MATERIAL = python_net_import('SMT.MastaAPI.Bearings', 'BearingCageMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCageMaterial',)


class BearingCageMaterial(Enum):
    '''BearingCageMaterial

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_CAGE_MATERIAL
    __hash__ = None

    STEEL = 0
    BRASS = 1
    PLASTIC = 2
