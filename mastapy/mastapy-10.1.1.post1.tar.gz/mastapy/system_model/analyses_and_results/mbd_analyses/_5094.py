'''_5094.py

TorqueConverterStatus
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_STATUS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterStatus')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterStatus',)


class TorqueConverterStatus(Enum):
    '''TorqueConverterStatus

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _TORQUE_CONVERTER_STATUS

    __hash__ = None

    FULLY_LOCKED = 0
    CURRENTLY_LOCKING = 1
    CURRENTLY_UNLOCKING = 2
    FULLY_UNLOCKED = 3
