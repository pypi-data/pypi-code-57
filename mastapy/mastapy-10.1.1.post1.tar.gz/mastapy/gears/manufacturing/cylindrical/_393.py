'''_393.py

CutterFlankSections
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CUTTER_FLANK_SECTIONS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CutterFlankSections')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterFlankSections',)


class CutterFlankSections(Enum):
    '''CutterFlankSections

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CUTTER_FLANK_SECTIONS

    __hash__ = None

    BOTTOM_LANDTOPPING = 0
    SEMITOPPING = 1
    MAIN_PROFILE = 2
    PROTUBERANCE_BLADE = 3
    TIP_FILLET = 4
    TOP_LAND = 5
