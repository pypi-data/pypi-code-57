'''_1802.py

GearMesh
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.system_model.connections_and_sockets import _1773
from mastapy._internal.python_net import python_net_import

_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMesh',)


class GearMesh(_1773.InterMountableComponentConnection):
    '''GearMesh

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMesh.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def user_specified_mesh_stiffness(self) -> 'float':
        '''float: 'UserSpecifiedMeshStiffness' is the original name of this property.'''

        return self.wrapped.UserSpecifiedMeshStiffness

    @user_specified_mesh_stiffness.setter
    def user_specified_mesh_stiffness(self, value: 'float'):
        self.wrapped.UserSpecifiedMeshStiffness = float(value) if value else 0.0

    @property
    def use_specified_mesh_stiffness(self) -> 'bool':
        '''bool: 'UseSpecifiedMeshStiffness' is the original name of this property.'''

        return self.wrapped.UseSpecifiedMeshStiffness

    @use_specified_mesh_stiffness.setter
    def use_specified_mesh_stiffness(self, value: 'bool'):
        self.wrapped.UseSpecifiedMeshStiffness = bool(value) if value else False

    @property
    def mesh_efficiency(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MeshEfficiency' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MeshEfficiency) if self.wrapped.MeshEfficiency else None

    @mesh_efficiency.setter
    def mesh_efficiency(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MeshEfficiency = value
