'''_6028.py

TorqueConverterLockupRule
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_LOCKUP_RULE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterLockupRule')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterLockupRule',)


class TorqueConverterLockupRule(Enum):
    '''TorqueConverterLockupRule

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TORQUE_CONVERTER_LOCKUP_RULE
    __hash__ = None

    SPECIFY_TIME = 0
    SPEED_RATIO_AND_VEHICLE_SPEED = 1
    PRESSURE_VS_TIME = 2
