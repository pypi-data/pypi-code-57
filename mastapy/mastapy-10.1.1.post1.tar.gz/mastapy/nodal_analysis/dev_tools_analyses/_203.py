'''_203.py

FESurfaceDrawingOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FE_SURFACE_DRAWING_OPTION = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'FESurfaceDrawingOption')


__docformat__ = 'restructuredtext en'
__all__ = ('FESurfaceDrawingOption',)


class FESurfaceDrawingOption(Enum):
    '''FESurfaceDrawingOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _FE_SURFACE_DRAWING_OPTION
    __hash__ = None

    NONE = 0
    TRANSPARENT = 1
    SOLID = 2
