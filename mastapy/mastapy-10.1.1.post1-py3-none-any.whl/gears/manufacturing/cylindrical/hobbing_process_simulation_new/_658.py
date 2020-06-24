'''_658.py

ActiveProcessMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ACTIVE_PROCESS_METHOD = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ActiveProcessMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveProcessMethod',)


class ActiveProcessMethod(Enum):
    '''ActiveProcessMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ACTIVE_PROCESS_METHOD
    __hash__ = None

    ROUGH_PROCESS_SIMULATION = 0
    FINISH_PROCESS_SIMULATION = 1
