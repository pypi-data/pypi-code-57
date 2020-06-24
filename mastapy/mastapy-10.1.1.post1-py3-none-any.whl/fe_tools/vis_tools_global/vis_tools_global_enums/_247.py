'''_247.py

ElementPropertiesShellWallType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_SHELL_WALL_TYPE = python_net_import('SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums', 'ElementPropertiesShellWallType')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesShellWallType',)


class ElementPropertiesShellWallType(Enum):
    '''ElementPropertiesShellWallType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ELEMENT_PROPERTIES_SHELL_WALL_TYPE
    __hash__ = None

    MONOCOQUE = 0
    LAMINATED = 2
