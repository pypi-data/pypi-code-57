'''_4734.py

CoordinateSystemForWhine
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_COORDINATE_SYSTEM_FOR_WHINE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CoordinateSystemForWhine')


__docformat__ = 'restructuredtext en'
__all__ = ('CoordinateSystemForWhine',)


class CoordinateSystemForWhine(Enum):
    '''CoordinateSystemForWhine

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _COORDINATE_SYSTEM_FOR_WHINE

    __hash__ = None

    LOCAL_COORDINATE_SYSTEM = 0
    GLOBAL_COORDINATE_SYSTEM = 1
