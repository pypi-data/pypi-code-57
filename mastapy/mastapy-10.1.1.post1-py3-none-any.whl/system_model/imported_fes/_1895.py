'''_1895.py

SystemDeflectionFEExportOptions
'''


from typing import Callable, List

from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item
from mastapy.nodal_analysis.fe_export_utility import _172, _173
from mastapy._internal import constructor, conversion
from mastapy.utility.units_and_measurements import _1385
from mastapy.system_model.imported_fes import _1888, _1887
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SYSTEM_DEFLECTION_FE_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'SystemDeflectionFEExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemDeflectionFEExportOptions',)


class SystemDeflectionFEExportOptions(_1.APIBase):
    '''SystemDeflectionFEExportOptions

    This is a mastapy class.
    '''

    TYPE = _SYSTEM_DEFLECTION_FE_EXPORT_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SystemDeflectionFEExportOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def default_type_of_result_to_export(self) -> 'enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType':
        '''enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType: 'DefaultTypeOfResultToExport' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType)(self.wrapped.DefaultTypeOfResultToExport) if self.wrapped.DefaultTypeOfResultToExport else None

    @default_type_of_result_to_export.setter
    def default_type_of_result_to_export(self, value: 'enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BoundaryConditionType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DefaultTypeOfResultToExport = value

    @property
    def include_rigid_coupling_nodes_and_constraints_added_by_masta(self) -> 'bool':
        '''bool: 'IncludeRigidCouplingNodesAndConstraintsAddedByMASTA' is the original name of this property.'''

        return self.wrapped.IncludeRigidCouplingNodesAndConstraintsAddedByMASTA

    @include_rigid_coupling_nodes_and_constraints_added_by_masta.setter
    def include_rigid_coupling_nodes_and_constraints_added_by_masta(self, value: 'bool'):
        self.wrapped.IncludeRigidCouplingNodesAndConstraintsAddedByMASTA = bool(value) if value else False

    @property
    def base_couplings_on_alternative_fe_mesh(self) -> 'bool':
        '''bool: 'BaseCouplingsOnAlternativeFEMesh' is the original name of this property.'''

        return self.wrapped.BaseCouplingsOnAlternativeFEMesh

    @base_couplings_on_alternative_fe_mesh.setter
    def base_couplings_on_alternative_fe_mesh(self, value: 'bool'):
        self.wrapped.BaseCouplingsOnAlternativeFEMesh = bool(value) if value else False

    @property
    def select_alternative_fe_mesh_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectAlternativeFEMeshFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectAlternativeFEMeshFile

    @property
    def alternative_fe_mesh_file(self) -> 'str':
        '''str: 'AlternativeFEMeshFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AlternativeFEMeshFile

    @property
    def include_an_fe_mesh(self) -> 'bool':
        '''bool: 'IncludeAnFEMesh' is the original name of this property.'''

        return self.wrapped.IncludeAnFEMesh

    @include_an_fe_mesh.setter
    def include_an_fe_mesh(self, value: 'bool'):
        self.wrapped.IncludeAnFEMesh = bool(value) if value else False

    @property
    def select_fe_mesh_file_to_include(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectFEMeshFileToInclude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectFEMeshFileToInclude

    @property
    def path_of_fe_mesh_file_to_be_included(self) -> 'str':
        '''str: 'PathOfFEMeshFileToBeIncluded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PathOfFEMeshFileToBeIncluded

    @property
    def length_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'LengthUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.LengthUnit) if self.wrapped.LengthUnit else None

    @length_unit.setter
    def length_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.LengthUnit = value

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
    def export_to_fe_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ExportToFEFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportToFEFile

    @property
    def nodes(self) -> 'List[_1888.PerNodeExportOptions]':
        '''List[PerNodeExportOptions]: 'Nodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Nodes, constructor.new(_1888.PerNodeExportOptions))
        return value

    @property
    def links(self) -> 'List[_1887.PerLinkExportOptions]':
        '''List[PerLinkExportOptions]: 'Links' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Links, constructor.new(_1887.PerLinkExportOptions))
        return value
