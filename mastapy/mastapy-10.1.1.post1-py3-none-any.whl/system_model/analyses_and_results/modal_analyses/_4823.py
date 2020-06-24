'''_4823.py

WhineWaterfallExportOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_WHINE_WATERFALL_EXPORT_OPTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'WhineWaterfallExportOption')


__docformat__ = 'restructuredtext en'
__all__ = ('WhineWaterfallExportOption',)


class WhineWaterfallExportOption(Enum):
    '''WhineWaterfallExportOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _WHINE_WATERFALL_EXPORT_OPTION

    __hash__ = None

    MATRIX = 0
    POINTS_LIST = 1
