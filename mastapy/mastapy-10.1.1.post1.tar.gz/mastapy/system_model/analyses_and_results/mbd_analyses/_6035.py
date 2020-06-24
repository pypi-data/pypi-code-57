'''_6035.py

WheelSlipType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_WHEEL_SLIP_TYPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'WheelSlipType')


__docformat__ = 'restructuredtext en'
__all__ = ('WheelSlipType',)


class WheelSlipType(Enum):
    '''WheelSlipType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _WHEEL_SLIP_TYPE
    __hash__ = None

    NO_SLIP = 0
    BASIC_SLIP = 1
