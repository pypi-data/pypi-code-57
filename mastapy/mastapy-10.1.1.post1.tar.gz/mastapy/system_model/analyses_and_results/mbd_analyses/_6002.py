'''_6002.py

RunUpDrivingMode
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RUN_UP_DRIVING_MODE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'RunUpDrivingMode')


__docformat__ = 'restructuredtext en'
__all__ = ('RunUpDrivingMode',)


class RunUpDrivingMode(Enum):
    '''RunUpDrivingMode

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _RUN_UP_DRIVING_MODE
    __hash__ = None

    TORQUE = 0
    SPEED = 1
