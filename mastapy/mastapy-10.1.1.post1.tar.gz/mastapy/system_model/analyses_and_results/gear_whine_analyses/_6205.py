'''_6205.py

GearWhineAnalysisFEExportOptions
'''


from typing import Callable, List

from mastapy._internal.implicit import list_with_selected_item, enum_with_selected_value
from mastapy.system_model.analyses_and_results.gear_whine_analyses import (
    _3803, _6206, _6185, _6184
)
from mastapy._internal import constructor, conversion
from mastapy.utility.units_and_measurements import _1385
from mastapy.nodal_analysis.fe_export_utility import _173
from mastapy.math_utility import _1221
from mastapy.nodal_analysis.dev_tools_analyses import _175
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS_FE_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GearWhineAnalysisFEExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysisFEExportOptions',)


class GearWhineAnalysisFEExportOptions(_1.APIBase):
    '''GearWhineAnalysisFEExportOptions

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS_FE_EXPORT_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysisFEExportOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def planetary_duplicate_to_export(self) -> 'list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis':
        '''list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis: 'PlanetaryDuplicateToExport' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis)(self.wrapped.PlanetaryDuplicateToExport) if self.wrapped.PlanetaryDuplicateToExport else None

    @planetary_duplicate_to_export.setter
    def planetary_duplicate_to_export(self, value: 'list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.PlanetaryDuplicateToExport = value

    @property
    def distance_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'DistanceUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.DistanceUnit) if self.wrapped.DistanceUnit else None

    @distance_unit.setter
    def distance_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.DistanceUnit = value

    @property
    def force_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'ForceUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.ForceUnit) if self.wrapped.ForceUnit else None

    @force_unit.setter
    def force_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ForceUnit = value

    @property
    def export_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType':
        '''enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType: 'ExportType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType)(self.wrapped.ExportType) if self.wrapped.ExportType else None

    @export_type.setter
    def export_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ExportType = value

    @property
    def complex_number_output_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput':
        '''enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput: 'ComplexNumberOutputOption' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput)(self.wrapped.ComplexNumberOutputOption) if self.wrapped.ComplexNumberOutputOption else None

    @complex_number_output_option.setter
    def complex_number_output_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ComplexNumberOutputOption = value

    @property
    def include_original_fe_file(self) -> 'bool':
        '''bool: 'IncludeOriginalFEFile' is the original name of this property.'''

        return self.wrapped.IncludeOriginalFEFile

    @include_original_fe_file.setter
    def include_original_fe_file(self, value: 'bool'):
        self.wrapped.IncludeOriginalFEFile = bool(value) if value else False

    @property
    def fe_export_format(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat':
        '''enum_with_selected_value.EnumWithSelectedValue_FEExportFormat: 'FEExportFormat' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_FEExportFormat)(self.wrapped.FEExportFormat) if self.wrapped.FEExportFormat else None

    @fe_export_format.setter
    def fe_export_format(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.FEExportFormat = value

    @property
    def include_rigid_couplings_and_nodes_added_by_masta(self) -> 'bool':
        '''bool: 'IncludeRigidCouplingsAndNodesAddedByMASTA' is the original name of this property.'''

        return self.wrapped.IncludeRigidCouplingsAndNodesAddedByMASTA

    @include_rigid_couplings_and_nodes_added_by_masta.setter
    def include_rigid_couplings_and_nodes_added_by_masta(self, value: 'bool'):
        self.wrapped.IncludeRigidCouplingsAndNodesAddedByMASTA = bool(value) if value else False

    @property
    def use_single_speed(self) -> 'bool':
        '''bool: 'UseSingleSpeed' is the original name of this property.'''

        return self.wrapped.UseSingleSpeed

    @use_single_speed.setter
    def use_single_speed(self, value: 'bool'):
        self.wrapped.UseSingleSpeed = bool(value) if value else False

    @property
    def reference_speed(self) -> 'float':
        '''float: 'ReferenceSpeed' is the original name of this property.'''

        return self.wrapped.ReferenceSpeed

    @reference_speed.setter
    def reference_speed(self, value: 'float'):
        self.wrapped.ReferenceSpeed = float(value) if value else 0.0

    @property
    def combine_excitations_of_same_order(self) -> 'bool':
        '''bool: 'CombineExcitationsOfSameOrder' is the original name of this property.'''

        return self.wrapped.CombineExcitationsOfSameOrder

    @combine_excitations_of_same_order.setter
    def combine_excitations_of_same_order(self, value: 'bool'):
        self.wrapped.CombineExcitationsOfSameOrder = bool(value) if value else False

    @property
    def export_results(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ExportResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportResults

    @property
    def status_message_for_export(self) -> 'str':
        '''str: 'StatusMessageForExport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StatusMessageForExport

    @property
    def type_of_result_to_export(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType':
        '''enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType: 'TypeOfResultToExport' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType)(self.wrapped.TypeOfResultToExport) if self.wrapped.TypeOfResultToExport else None

    @type_of_result_to_export.setter
    def type_of_result_to_export(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.TypeOfResultToExport = value

    @property
    def analysis_options(self) -> '_6206.GearWhineAnalysisOptions':
        '''GearWhineAnalysisOptions: 'AnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6206.GearWhineAnalysisOptions)(self.wrapped.AnalysisOptions) if self.wrapped.AnalysisOptions else None

    @property
    def reference_speed_options(self) -> '_6185.SpeedOptionsForGearWhineAnalysisResults':
        '''SpeedOptionsForGearWhineAnalysisResults: 'ReferenceSpeedOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6185.SpeedOptionsForGearWhineAnalysisResults)(self.wrapped.ReferenceSpeedOptions) if self.wrapped.ReferenceSpeedOptions else None

    @property
    def frequency_options(self) -> '_6184.FrequencyOptionsForGearWhineAnalysisResults':
        '''FrequencyOptionsForGearWhineAnalysisResults: 'FrequencyOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6184.FrequencyOptionsForGearWhineAnalysisResults)(self.wrapped.FrequencyOptions) if self.wrapped.FrequencyOptions else None

    @property
    def eigenvalue_options(self) -> '_175.EigenvalueOptions':
        '''EigenvalueOptions: 'EigenvalueOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_175.EigenvalueOptions)(self.wrapped.EigenvalueOptions) if self.wrapped.EigenvalueOptions else None

    def export_to_folder(self, folder_path: 'str') -> 'List[str]':
        ''' 'ExportToFolder' is the original name of this method.

        Args:
            folder_path (str)

        Returns:
            List[str]
        '''

        folder_path = str(folder_path)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.ExportToFolder(folder_path if folder_path else None), str)
