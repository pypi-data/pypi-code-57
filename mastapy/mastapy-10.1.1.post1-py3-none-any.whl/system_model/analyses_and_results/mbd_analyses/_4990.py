'''_4990.py

ClutchSpringType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CLUTCH_SPRING_TYPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ClutchSpringType')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchSpringType',)


class ClutchSpringType(Enum):
    '''ClutchSpringType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CLUTCH_SPRING_TYPE

    __hash__ = None

    NONE = 0
    SPRUNG_APART = 1
