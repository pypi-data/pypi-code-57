'''_1961.py

NodeSelectionDepthOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_NODE_SELECTION_DEPTH_OPTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'NodeSelectionDepthOption')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeSelectionDepthOption',)


class NodeSelectionDepthOption(Enum):
    '''NodeSelectionDepthOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _NODE_SELECTION_DEPTH_OPTION

    __hash__ = None

    SURFACE_NODES = 0
    SOLID_NODES = 1
