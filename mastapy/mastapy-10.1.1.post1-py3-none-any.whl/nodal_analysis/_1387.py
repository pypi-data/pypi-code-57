'''_1387.py

ResultLoggingFrequency
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RESULT_LOGGING_FREQUENCY = python_net_import('SMT.MastaAPI.NodalAnalysis', 'ResultLoggingFrequency')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultLoggingFrequency',)


class ResultLoggingFrequency(Enum):
    '''ResultLoggingFrequency

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _RESULT_LOGGING_FREQUENCY

    __hash__ = None

    ALL = 0
    IGNORE_SMALL_STEPS = 1
    NONE = 2
