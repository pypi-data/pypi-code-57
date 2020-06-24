'''_6278.py

HarmonicLoadDataImportBase
'''


from typing import Callable, Generic, TypeVar

from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy import _1
from mastapy.system_model.analyses_and_results.static_loads import _6269
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_IMPORT_BASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataImportBase')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataImportBase',)


T = TypeVar('T', bound='_6269.ElectricMachineHarmonicLoadImportOptionsBase')


class HarmonicLoadDataImportBase(_1.APIBase, Generic[T]):
    '''HarmonicLoadDataImportBase

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _HARMONIC_LOAD_DATA_IMPORT_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataImportBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def file_name(self) -> 'str':
        '''str: 'FileName' is the original name of this property.'''

        return self.wrapped.FileName

    @file_name.setter
    def file_name(self, value: 'str'):
        self.wrapped.FileName = str(value) if value else None

    @property
    def read_data_from_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ReadDataFromFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReadDataFromFile

    @property
    def negate_torque_data_on_import(self) -> 'bool':
        '''bool: 'NegateTorqueDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateTorqueDataOnImport

    @negate_torque_data_on_import.setter
    def negate_torque_data_on_import(self, value: 'bool'):
        self.wrapped.NegateTorqueDataOnImport = bool(value) if value else False

    @property
    def negate_stator_radial_load_data_on_import(self) -> 'bool':
        '''bool: 'NegateStatorRadialLoadDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateStatorRadialLoadDataOnImport

    @negate_stator_radial_load_data_on_import.setter
    def negate_stator_radial_load_data_on_import(self, value: 'bool'):
        self.wrapped.NegateStatorRadialLoadDataOnImport = bool(value) if value else False

    @property
    def negate_stator_tangential_load_data_on_import(self) -> 'bool':
        '''bool: 'NegateStatorTangentialLoadDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateStatorTangentialLoadDataOnImport

    @negate_stator_tangential_load_data_on_import.setter
    def negate_stator_tangential_load_data_on_import(self, value: 'bool'):
        self.wrapped.NegateStatorTangentialLoadDataOnImport = bool(value) if value else False

    @property
    def negate_stator_axial_load_data_on_import(self) -> 'bool':
        '''bool: 'NegateStatorAxialLoadDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateStatorAxialLoadDataOnImport

    @negate_stator_axial_load_data_on_import.setter
    def negate_stator_axial_load_data_on_import(self, value: 'bool'):
        self.wrapped.NegateStatorAxialLoadDataOnImport = bool(value) if value else False

    @property
    def negate_speed_data_on_import(self) -> 'bool':
        '''bool: 'NegateSpeedDataOnImport' is the original name of this property.'''

        return self.wrapped.NegateSpeedDataOnImport

    @negate_speed_data_on_import.setter
    def negate_speed_data_on_import(self, value: 'bool'):
        self.wrapped.NegateSpeedDataOnImport = bool(value) if value else False

    @property
    def node_id_of_first_tooth(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'NodeIdOfFirstTooth' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.NodeIdOfFirstTooth) if self.wrapped.NodeIdOfFirstTooth else None

    @node_id_of_first_tooth.setter
    def node_id_of_first_tooth(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.NodeIdOfFirstTooth = value

    @property
    def imported_data_has_different_direction_for_tooth_ids_to_masta_model(self) -> 'bool':
        '''bool: 'ImportedDataHasDifferentDirectionForToothIdsToMASTAModel' is the original name of this property.'''

        return self.wrapped.ImportedDataHasDifferentDirectionForToothIdsToMASTAModel

    @imported_data_has_different_direction_for_tooth_ids_to_masta_model.setter
    def imported_data_has_different_direction_for_tooth_ids_to_masta_model(self, value: 'bool'):
        self.wrapped.ImportedDataHasDifferentDirectionForToothIdsToMASTAModel = bool(value) if value else False
