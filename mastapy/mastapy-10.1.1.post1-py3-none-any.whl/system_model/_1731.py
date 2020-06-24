'''_1731.py

MeshStiffnessModel
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MESH_STIFFNESS_MODEL = python_net_import('SMT.MastaAPI.SystemModel', 'MeshStiffnessModel')


__docformat__ = 'restructuredtext en'
__all__ = ('MeshStiffnessModel',)


class MeshStiffnessModel(Enum):
    '''MeshStiffnessModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MESH_STIFFNESS_MODEL
    __hash__ = None

    CONSTANT_IN_LOA = 0
    ADVANCED_SYSTEM_DEFLECTION = 1
    ISO_SIMPLE_CONTINUOUS_MODEL = 2
