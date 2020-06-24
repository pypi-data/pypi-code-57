'''_1871.py

ImportedFEStiffnessNode
'''


from mastapy._internal import constructor, conversion
from mastapy._internal.vector_3d import Vector3D
from mastapy.math_utility.measured_vectors import _1253
from mastapy.utility.units_and_measurements.measurements import _1302, _1366
from mastapy.nodal_analysis import _92
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_STIFFNESS_NODE = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEStiffnessNode')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEStiffnessNode',)


class ImportedFEStiffnessNode(_92.FEStiffnessNode):
    '''ImportedFEStiffnessNode

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_STIFFNESS_NODE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEStiffnessNode.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def external_id(self) -> 'int':
        '''int: 'ExternalID' is the original name of this property.'''

        return self.wrapped.ExternalID

    @external_id.setter
    def external_id(self, value: 'int'):
        self.wrapped.ExternalID = int(value) if value else 0

    @property
    def override_default_name(self) -> 'bool':
        '''bool: 'OverrideDefaultName' is the original name of this property.'''

        return self.wrapped.OverrideDefaultName

    @override_default_name.setter
    def override_default_name(self, value: 'bool'):
        self.wrapped.OverrideDefaultName = bool(value) if value else False

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def position_in_world_coordinate_system(self) -> 'Vector3D':
        '''Vector3D: 'PositionInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.PositionInWorldCoordinateSystem)
        return value

    @property
    def force_due_to_gravity_in_local_coordinate_system(self) -> '_1253.VectorWithLinearAndAngularComponents[_1302.Force, _1366.Torque]':
        '''VectorWithLinearAndAngularComponents[Force, Torque]: 'ForceDueToGravityInLocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1253.VectorWithLinearAndAngularComponents)[_1302.Force, _1366.Torque](self.wrapped.ForceDueToGravityInLocalCoordinateSystem) if self.wrapped.ForceDueToGravityInLocalCoordinateSystem else None

    @property
    def force_due_to_gravity_in_local_coordinate_system_with_gravity_in_fe_x_direction(self) -> '_1253.VectorWithLinearAndAngularComponents[_1302.Force, _1366.Torque]':
        '''VectorWithLinearAndAngularComponents[Force, Torque]: 'ForceDueToGravityInLocalCoordinateSystemWithGravityInFEXDirection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1253.VectorWithLinearAndAngularComponents)[_1302.Force, _1366.Torque](self.wrapped.ForceDueToGravityInLocalCoordinateSystemWithGravityInFEXDirection) if self.wrapped.ForceDueToGravityInLocalCoordinateSystemWithGravityInFEXDirection else None

    @property
    def force_due_to_gravity_in_local_coordinate_system_with_gravity_in_fe_y_direction(self) -> '_1253.VectorWithLinearAndAngularComponents[_1302.Force, _1366.Torque]':
        '''VectorWithLinearAndAngularComponents[Force, Torque]: 'ForceDueToGravityInLocalCoordinateSystemWithGravityInFEYDirection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1253.VectorWithLinearAndAngularComponents)[_1302.Force, _1366.Torque](self.wrapped.ForceDueToGravityInLocalCoordinateSystemWithGravityInFEYDirection) if self.wrapped.ForceDueToGravityInLocalCoordinateSystemWithGravityInFEYDirection else None

    @property
    def force_due_to_gravity_in_local_coordinate_system_with_gravity_in_fe_z_direction(self) -> '_1253.VectorWithLinearAndAngularComponents[_1302.Force, _1366.Torque]':
        '''VectorWithLinearAndAngularComponents[Force, Torque]: 'ForceDueToGravityInLocalCoordinateSystemWithGravityInFEZDirection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1253.VectorWithLinearAndAngularComponents)[_1302.Force, _1366.Torque](self.wrapped.ForceDueToGravityInLocalCoordinateSystemWithGravityInFEZDirection) if self.wrapped.ForceDueToGravityInLocalCoordinateSystemWithGravityInFEZDirection else None
