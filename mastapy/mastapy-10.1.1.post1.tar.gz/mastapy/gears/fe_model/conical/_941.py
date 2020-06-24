'''_941.py

FlankDataSource
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FLANK_DATA_SOURCE = python_net_import('SMT.MastaAPI.Gears.FEModel.Conical', 'FlankDataSource')


__docformat__ = 'restructuredtext en'
__all__ = ('FlankDataSource',)


class FlankDataSource(Enum):
    '''FlankDataSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _FLANK_DATA_SOURCE

    __hash__ = None

    MACRODESIGN = 0
    MANUFACTURING = 1
