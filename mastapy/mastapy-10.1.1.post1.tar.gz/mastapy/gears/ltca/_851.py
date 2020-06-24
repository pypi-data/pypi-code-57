'''_851.py

CylindricalMeshedGearLoadDistributionAnalysis
'''


from mastapy._internal import constructor, conversion
from mastapy.gears.cylindrical import _892, _893
from mastapy.gears.ltca import _850
from mastapy.math_utility import _894
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESHED_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'CylindricalMeshedGearLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshedGearLoadDistributionAnalysis',)


class CylindricalMeshedGearLoadDistributionAnalysis(_1.APIBase):
    '''CylindricalMeshedGearLoadDistributionAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MESHED_GEAR_LOAD_DISTRIBUTION_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalMeshedGearLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def nominal_torque(self) -> 'float':
        '''float: 'NominalTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NominalTorque

    @property
    def torque_scaled_by_application_and_dynamic_factors(self) -> 'float':
        '''float: 'TorqueScaledByApplicationAndDynamicFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueScaledByApplicationAndDynamicFactors

    @property
    def is_loaded_on_tip(self) -> 'bool':
        '''bool: 'IsLoadedOnTip' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLoadedOnTip

    @property
    def maximum_von_mises_root_stress_tension(self) -> 'float':
        '''float: 'MaximumVonMisesRootStressTension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumVonMisesRootStressTension

    @property
    def maximum_principal_root_stress_tension(self) -> 'float':
        '''float: 'MaximumPrincipalRootStressTension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumPrincipalRootStressTension

    @property
    def maximum_von_mises_root_stress_compression(self) -> 'float':
        '''float: 'MaximumVonMisesRootStressCompression' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumVonMisesRootStressCompression

    @property
    def maximum_principal_root_stress_compression(self) -> 'float':
        '''float: 'MaximumPrincipalRootStressCompression' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumPrincipalRootStressCompression

    @property
    def contact_charts(self) -> '_892.CylindricalGearLTCAContactCharts':
        '''CylindricalGearLTCAContactCharts: 'ContactCharts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_892.CylindricalGearLTCAContactCharts)(self.wrapped.ContactCharts) if self.wrapped.ContactCharts else None

    @property
    def contact_charts_as_text_file(self) -> '_893.CylindricalGearLTCAContactChartDataAsTextFile':
        '''CylindricalGearLTCAContactChartDataAsTextFile: 'ContactChartsAsTextFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_893.CylindricalGearLTCAContactChartDataAsTextFile)(self.wrapped.ContactChartsAsTextFile) if self.wrapped.ContactChartsAsTextFile else None

    def contact_patch_detailed(self, result_type: '_850.ContactResultType', number_of_face_width_steps: 'int', number_of_roll_distance_steps: 'int') -> '_894.GriddedSurface':
        ''' 'ContactPatch' is the original name of this method.

        Args:
            result_type (mastapy.gears.ltca.ContactResultType)
            number_of_face_width_steps (int)
            number_of_roll_distance_steps (int)

        Returns:
            mastapy.math_utility.GriddedSurface
        '''

        result_type = conversion.mp_to_pn_enum(result_type)
        number_of_face_width_steps = int(number_of_face_width_steps)
        number_of_roll_distance_steps = int(number_of_roll_distance_steps)
        method_result = self.wrapped.ContactPatch(result_type, number_of_face_width_steps if number_of_face_width_steps else 0, number_of_roll_distance_steps if number_of_roll_distance_steps else 0)
        return constructor.new(_894.GriddedSurface)(method_result) if method_result else None

    def contact_patch(self, result_type: '_850.ContactResultType', include_tip_contact: 'bool') -> '_894.GriddedSurface':
        ''' 'ContactPatch' is the original name of this method.

        Args:
            result_type (mastapy.gears.ltca.ContactResultType)
            include_tip_contact (bool)

        Returns:
            mastapy.math_utility.GriddedSurface
        '''

        result_type = conversion.mp_to_pn_enum(result_type)
        include_tip_contact = bool(include_tip_contact)
        method_result = self.wrapped.ContactPatch(result_type, include_tip_contact if include_tip_contact else False)
        return constructor.new(_894.GriddedSurface)(method_result) if method_result else None

    def contact_patch_as_text(self, result_type: '_850.ContactResultType', include_tip_contact: 'bool', file_name_with_path: 'str'):
        ''' 'ContactPatchAsText' is the original name of this method.

        Args:
            result_type (mastapy.gears.ltca.ContactResultType)
            include_tip_contact (bool)
            file_name_with_path (str)
        '''

        result_type = conversion.mp_to_pn_enum(result_type)
        include_tip_contact = bool(include_tip_contact)
        file_name_with_path = str(file_name_with_path)
        self.wrapped.ContactPatchAsText(result_type, include_tip_contact if include_tip_contact else False, file_name_with_path if file_name_with_path else None)
