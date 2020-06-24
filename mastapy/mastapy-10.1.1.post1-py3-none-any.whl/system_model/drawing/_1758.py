'''_1758.py

StressResultOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_STRESS_RESULT_OPTION = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'StressResultOption')


__docformat__ = 'restructuredtext en'
__all__ = ('StressResultOption',)


class StressResultOption(Enum):
    '''StressResultOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _STRESS_RESULT_OPTION
    __hash__ = None

    ELEMENT_NODE = 0
    AVERAGE_TO_NODES = 1
