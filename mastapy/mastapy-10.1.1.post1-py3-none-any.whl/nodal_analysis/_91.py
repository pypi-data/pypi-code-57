'''_91.py

FEStiffness
'''


from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis import _95, _109
from mastapy._internal.vector_3d import Vector3D
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FE_STIFFNESS = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FEStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('FEStiffness',)


class FEStiffness(_1.APIBase):
    '''FEStiffness

    This is a mastapy class.
    '''

    TYPE = _FE_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def radial_alignment_tolerance(self) -> 'float':
        '''float: 'RadialAlignmentTolerance' is the original name of this property.'''

        return self.wrapped.RadialAlignmentTolerance

    @radial_alignment_tolerance.setter
    def radial_alignment_tolerance(self, value: 'float'):
        self.wrapped.RadialAlignmentTolerance = float(value) if value else 0.0

    @property
    def axial_alignment_tolerance(self) -> 'float':
        '''float: 'AxialAlignmentTolerance' is the original name of this property.'''

        return self.wrapped.AxialAlignmentTolerance

    @axial_alignment_tolerance.setter
    def axial_alignment_tolerance(self, value: 'float'):
        self.wrapped.AxialAlignmentTolerance = float(value) if value else 0.0

    @property
    def is_grounded(self) -> 'bool':
        '''bool: 'IsGrounded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsGrounded

    @property
    def tolerance_for_zero_frequencies(self) -> 'float':
        '''float: 'ToleranceForZeroFrequencies' is the original name of this property.'''

        return self.wrapped.ToleranceForZeroFrequencies

    @tolerance_for_zero_frequencies.setter
    def tolerance_for_zero_frequencies(self, value: 'float'):
        self.wrapped.ToleranceForZeroFrequencies = float(value) if value else 0.0

    @property
    def mass_matrix_is_known(self) -> 'bool':
        '''bool: 'MassMatrixIsKnown' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassMatrixIsKnown

    @property
    def gyroscopic_matrix_is_known(self) -> 'bool':
        '''bool: 'GyroscopicMatrixIsKnown' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GyroscopicMatrixIsKnown

    @property
    def gravity_force_is_known(self) -> 'bool':
        '''bool: 'GravityForceIsKnown' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GravityForceIsKnown

    @property
    def gravity_force_source(self) -> '_95.GravityForceSource':
        '''GravityForceSource: 'GravityForceSource' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.GravityForceSource)
        return constructor.new(_95.GravityForceSource)(value) if value else None

    @property
    def gravity_force_can_be_rotated(self) -> 'bool':
        '''bool: 'GravityForceCanBeRotated' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GravityForceCanBeRotated

    @property
    def number_of_physical_nodes(self) -> 'int':
        '''int: 'NumberOfPhysicalNodes' is the original name of this property.'''

        return self.wrapped.NumberOfPhysicalNodes

    @number_of_physical_nodes.setter
    def number_of_physical_nodes(self, value: 'int'):
        self.wrapped.NumberOfPhysicalNodes = int(value) if value else 0

    @property
    def number_of_internal_modes(self) -> 'int':
        '''int: 'NumberOfInternalModes' is the original name of this property.'''

        return self.wrapped.NumberOfInternalModes

    @number_of_internal_modes.setter
    def number_of_internal_modes(self, value: 'int'):
        self.wrapped.NumberOfInternalModes = int(value) if value else 0

    @property
    def frequency_of_highest_mode(self) -> 'float':
        '''float: 'FrequencyOfHighestMode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FrequencyOfHighestMode

    @property
    def reason_scalar_mass_not_known(self) -> 'str':
        '''str: 'ReasonScalarMassNotKnown' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReasonScalarMassNotKnown

    @property
    def mass(self) -> 'float':
        '''float: 'Mass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Mass

    @property
    def calculate_acceleration_force_from_mass_matrix(self) -> 'bool':
        '''bool: 'CalculateAccelerationForceFromMassMatrix' is the original name of this property.'''

        return self.wrapped.CalculateAccelerationForceFromMassMatrix

    @calculate_acceleration_force_from_mass_matrix.setter
    def calculate_acceleration_force_from_mass_matrix(self, value: 'bool'):
        self.wrapped.CalculateAccelerationForceFromMassMatrix = bool(value) if value else False

    @property
    def is_using_full_fe_model(self) -> 'bool':
        '''bool: 'IsUsingFullFEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsUsingFullFEModel

    @property
    def reduced_stiffness_file_editable(self) -> 'str':
        '''str: 'ReducedStiffnessFileEditable' is the original name of this property.'''

        return self.wrapped.ReducedStiffnessFileEditable

    @reduced_stiffness_file_editable.setter
    def reduced_stiffness_file_editable(self, value: 'str'):
        self.wrapped.ReducedStiffnessFileEditable = str(value) if value else None

    @property
    def reduced_stiffness_file(self) -> 'str':
        '''str: 'ReducedStiffnessFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReducedStiffnessFile

    @property
    def stiffness_in_fe_coordinate_system_mn_rad(self) -> '_109.NodalMatrix':
        '''NodalMatrix: 'StiffnessInFECoordinateSystemMNRad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_109.NodalMatrix)(self.wrapped.StiffnessInFECoordinateSystemMNRad) if self.wrapped.StiffnessInFECoordinateSystemMNRad else None

    @property
    def mass_matrix_mn_rad_s_kg(self) -> '_109.NodalMatrix':
        '''NodalMatrix: 'MassMatrixMNRadSKg' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_109.NodalMatrix)(self.wrapped.MassMatrixMNRadSKg) if self.wrapped.MassMatrixMNRadSKg else None

    @property
    def centre_of_mass_in_local_coordinate_system(self) -> 'Vector3D':
        '''Vector3D: 'CentreOfMassInLocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.CentreOfMassInLocalCoordinateSystem)
        return value

    @property
    def stiffness_matrix(self) -> '_109.NodalMatrix':
        '''NodalMatrix: 'StiffnessMatrix' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_109.NodalMatrix)(self.wrapped.StiffnessMatrix) if self.wrapped.StiffnessMatrix else None
