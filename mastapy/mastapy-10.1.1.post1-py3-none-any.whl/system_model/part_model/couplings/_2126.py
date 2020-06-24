'''_2126.py

RigidConnectorTiltStiffnessTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RIGID_CONNECTOR_TILT_STIFFNESS_TYPES = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RigidConnectorTiltStiffnessTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('RigidConnectorTiltStiffnessTypes',)


class RigidConnectorTiltStiffnessTypes(Enum):
    '''RigidConnectorTiltStiffnessTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _RIGID_CONNECTOR_TILT_STIFFNESS_TYPES

    __hash__ = None

    SINGLE_NODE_WITH_SPECIFIED_STIFFNESS = 0
    DERIVED_FROM_LENGTH_AND_RADIAL_STIFFNESS = 1
