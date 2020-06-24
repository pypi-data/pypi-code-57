'''_92.py

FEStiffnessNode
'''


from mastapy._internal import constructor, conversion
from mastapy._internal.vector_3d import Vector3D
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FE_STIFFNESS_NODE = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FEStiffnessNode')


__docformat__ = 'restructuredtext en'
__all__ = ('FEStiffnessNode',)


class FEStiffnessNode(_1.APIBase):
    '''FEStiffnessNode

    This is a mastapy class.
    '''

    TYPE = _FE_STIFFNESS_NODE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEStiffnessNode.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_degrees_of_freedom(self) -> 'int':
        '''int: 'NumberOfDegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfDegreesOfFreedom

    @property
    def position_in_local_coordinate_system(self) -> 'Vector3D':
        '''Vector3D: 'PositionInLocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.PositionInLocalCoordinateSystem)
        return value

    @property
    def node_index(self) -> 'int':
        '''int: 'NodeIndex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NodeIndex
