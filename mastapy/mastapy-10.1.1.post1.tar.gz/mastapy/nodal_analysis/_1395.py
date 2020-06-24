'''_1395.py

VolumeElementShape
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_VOLUME_ELEMENT_SHAPE = python_net_import('SMT.MastaAPI.NodalAnalysis', 'VolumeElementShape')


__docformat__ = 'restructuredtext en'
__all__ = ('VolumeElementShape',)


class VolumeElementShape(Enum):
    '''VolumeElementShape

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _VOLUME_ELEMENT_SHAPE

    __hash__ = None

    TETRAHEDRAL = 0
    HEXAHEDRAL = 1
