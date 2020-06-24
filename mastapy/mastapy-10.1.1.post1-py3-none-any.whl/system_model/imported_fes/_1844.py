'''_1844.py

ComponentOrientationOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_COMPONENT_ORIENTATION_OPTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ComponentOrientationOption')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentOrientationOption',)


class ComponentOrientationOption(Enum):
    '''ComponentOrientationOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _COMPONENT_ORIENTATION_OPTION
    __hash__ = None

    DO_NOT_CHANGE = 0
    ALIGN_WITH_FE_AXES = 1
    ALIGN_NORMAL_TO_FE_SURFACE = 2
