'''_5031.py

InputSignalFilterLevel
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_INPUT_SIGNAL_FILTER_LEVEL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'InputSignalFilterLevel')


__docformat__ = 'restructuredtext en'
__all__ = ('InputSignalFilterLevel',)


class InputSignalFilterLevel(Enum):
    '''InputSignalFilterLevel

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _INPUT_SIGNAL_FILTER_LEVEL

    __hash__ = None

    NONE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
