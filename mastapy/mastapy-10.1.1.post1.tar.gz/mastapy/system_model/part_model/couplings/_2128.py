'''_2128.py

RigidConnectorToothSpacingType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RIGID_CONNECTOR_TOOTH_SPACING_TYPE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RigidConnectorToothSpacingType')


__docformat__ = 'restructuredtext en'
__all__ = ('RigidConnectorToothSpacingType',)


class RigidConnectorToothSpacingType(Enum):
    '''RigidConnectorToothSpacingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _RIGID_CONNECTOR_TOOTH_SPACING_TYPE

    __hash__ = None

    EQUALLYSPACED_TEETH = 0
    CUSTOM_SPACING_OF_TEETH = 1
