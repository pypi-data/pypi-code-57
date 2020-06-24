'''_101.py

MeshingDiameterForGear
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MESHING_DIAMETER_FOR_GEAR = python_net_import('SMT.MastaAPI.NodalAnalysis', 'MeshingDiameterForGear')


__docformat__ = 'restructuredtext en'
__all__ = ('MeshingDiameterForGear',)


class MeshingDiameterForGear(Enum):
    '''MeshingDiameterForGear

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MESHING_DIAMETER_FOR_GEAR
    __hash__ = None

    ROOT_DIAMETER = 0
    TIP_DIAMETER = 1
    REFERENCE_DIAMETER = 2
