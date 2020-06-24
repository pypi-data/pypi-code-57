'''_1130.py

ExternalFullFEFileOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_EXTERNAL_FULL_FE_FILE_OPTION = python_net_import('SMT.MastaAPI.Utility', 'ExternalFullFEFileOption')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalFullFEFileOption',)


class ExternalFullFEFileOption(Enum):
    '''ExternalFullFEFileOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _EXTERNAL_FULL_FE_FILE_OPTION

    __hash__ = None

    NONE = 0
    MESH = 1
    MESH_AND_EXPANSION_VECTORS = 2
