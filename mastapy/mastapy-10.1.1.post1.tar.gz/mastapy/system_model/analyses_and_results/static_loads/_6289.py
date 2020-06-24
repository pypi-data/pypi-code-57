'''_6289.py

TorqueSpecificationForSystemDeflection
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TORQUE_SPECIFICATION_FOR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueSpecificationForSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueSpecificationForSystemDeflection',)


class TorqueSpecificationForSystemDeflection(Enum):
    '''TorqueSpecificationForSystemDeflection

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TORQUE_SPECIFICATION_FOR_SYSTEM_DEFLECTION
    __hash__ = None

    CURRENT_TIME = 0
    SPECIFIED_ANGLE = 1
    SPECIFIED_TIME = 2
    MEAN = 3
    ROOT_MEAN_SQUARE = 4
