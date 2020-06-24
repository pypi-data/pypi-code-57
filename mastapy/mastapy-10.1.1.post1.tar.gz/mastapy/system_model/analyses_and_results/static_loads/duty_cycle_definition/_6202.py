'''_6202.py

TimeSeriesImporter
'''


from typing import Callable, List

from mastapy.system_model.analyses_and_results.static_loads import _6283
from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
    _6293, _6303, _6295, _6292,
    _6296, _6298, _6304, _6302,
    _6294, _6297, _6291
)
from mastapy.utility.file_access_helpers import _1441
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_TIME_SERIES_IMPORTER = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'TimeSeriesImporter')


__docformat__ = 'restructuredtext en'
__all__ = ('TimeSeriesImporter',)


class TimeSeriesImporter(_1.APIBase):
    '''TimeSeriesImporter

    This is a mastapy class.
    '''

    TYPE = _TIME_SERIES_IMPORTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TimeSeriesImporter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def import_type(self) -> '_6283.ImportType':
        '''ImportType: 'ImportType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ImportType)
        return constructor.new(_6283.ImportType)(value) if value else None

    @import_type.setter
    def import_type(self, value: '_6283.ImportType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ImportType = value

    @property
    def number_of_data_files(self) -> 'int':
        '''int: 'NumberOfDataFiles' is the original name of this property.'''

        return self.wrapped.NumberOfDataFiles

    @number_of_data_files.setter
    def number_of_data_files(self, value: 'int'):
        self.wrapped.NumberOfDataFiles = int(value) if value else 0

    @property
    def specify_load_case_names(self) -> 'bool':
        '''bool: 'SpecifyLoadCaseNames' is the original name of this property.'''

        return self.wrapped.SpecifyLoadCaseNames

    @specify_load_case_names.setter
    def specify_load_case_names(self, value: 'bool'):
        self.wrapped.SpecifyLoadCaseNames = bool(value) if value else False

    @property
    def number_of_extra_points_for_ramp_sections(self) -> 'int':
        '''int: 'NumberOfExtraPointsForRampSections' is the original name of this property.'''

        return self.wrapped.NumberOfExtraPointsForRampSections

    @number_of_extra_points_for_ramp_sections.setter
    def number_of_extra_points_for_ramp_sections(self, value: 'int'):
        self.wrapped.NumberOfExtraPointsForRampSections = int(value) if value else 0

    @property
    def number_of_cycle_repeats(self) -> 'float':
        '''float: 'NumberOfCycleRepeats' is the original name of this property.'''

        return self.wrapped.NumberOfCycleRepeats

    @number_of_cycle_repeats.setter
    def number_of_cycle_repeats(self, value: 'float'):
        self.wrapped.NumberOfCycleRepeats = float(value) if value else 0.0

    @property
    def number_of_torque_inputs(self) -> 'int':
        '''int: 'NumberOfTorqueInputs' is the original name of this property.'''

        return self.wrapped.NumberOfTorqueInputs

    @number_of_torque_inputs.setter
    def number_of_torque_inputs(self, value: 'int'):
        self.wrapped.NumberOfTorqueInputs = int(value) if value else 0

    @property
    def number_of_speed_inputs(self) -> 'int':
        '''int: 'NumberOfSpeedInputs' is the original name of this property.'''

        return self.wrapped.NumberOfSpeedInputs

    @number_of_speed_inputs.setter
    def number_of_speed_inputs(self, value: 'int'):
        self.wrapped.NumberOfSpeedInputs = int(value) if value else 0

    @property
    def number_of_force_inputs(self) -> 'int':
        '''int: 'NumberOfForceInputs' is the original name of this property.'''

        return self.wrapped.NumberOfForceInputs

    @number_of_force_inputs.setter
    def number_of_force_inputs(self, value: 'int'):
        self.wrapped.NumberOfForceInputs = int(value) if value else 0

    @property
    def number_of_moment_inputs(self) -> 'int':
        '''int: 'NumberOfMomentInputs' is the original name of this property.'''

        return self.wrapped.NumberOfMomentInputs

    @number_of_moment_inputs.setter
    def number_of_moment_inputs(self, value: 'int'):
        self.wrapped.NumberOfMomentInputs = int(value) if value else 0

    @property
    def number_of_boost_pressure_inputs(self) -> 'int':
        '''int: 'NumberOfBoostPressureInputs' is the original name of this property.'''

        return self.wrapped.NumberOfBoostPressureInputs

    @number_of_boost_pressure_inputs.setter
    def number_of_boost_pressure_inputs(self, value: 'int'):
        self.wrapped.NumberOfBoostPressureInputs = int(value) if value else 0

    @property
    def design_state_name(self) -> 'str':
        '''str: 'DesignStateName' is the original name of this property.'''

        return self.wrapped.DesignStateName

    @design_state_name.setter
    def design_state_name(self, value: 'str'):
        self.wrapped.DesignStateName = str(value) if value else None

    @property
    def duty_cycle_duration(self) -> 'float':
        '''float: 'DutyCycleDuration' is the original name of this property.'''

        return self.wrapped.DutyCycleDuration

    @duty_cycle_duration.setter
    def duty_cycle_duration(self, value: 'float'):
        self.wrapped.DutyCycleDuration = float(value) if value else 0.0

    @property
    def create_load_cases(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateLoadCases

    @property
    def destination_design_state_column(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState':
        '''enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState: 'DestinationDesignStateColumn' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState)(self.wrapped.DestinationDesignStateColumn) if self.wrapped.DestinationDesignStateColumn else None

    @destination_design_state_column.setter
    def destination_design_state_column(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DestinationDesignStateColumn = value

    @property
    def gear_ratios(self) -> 'str':
        '''str: 'GearRatios' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GearRatios

    @property
    def time_step_input(self) -> '_6303.TimeStepInputOptions':
        '''TimeStepInputOptions: 'TimeStepInput' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6303.TimeStepInputOptions)(self.wrapped.TimeStepInput) if self.wrapped.TimeStepInput else None

    @property
    def gear_ratio_options(self) -> '_6295.GearRatioInputOptions':
        '''GearRatioInputOptions: 'GearRatioOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6295.GearRatioInputOptions)(self.wrapped.GearRatioOptions) if self.wrapped.GearRatioOptions else None

    @property
    def design_state_options(self) -> '_6292.DesignStateOptions':
        '''DesignStateOptions: 'DesignStateOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6292.DesignStateOptions)(self.wrapped.DesignStateOptions) if self.wrapped.DesignStateOptions else None

    @property
    def load_case_name_inputs(self) -> '_6296.LoadCaseNameOptions':
        '''LoadCaseNameOptions: 'LoadCaseNameInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6296.LoadCaseNameOptions)(self.wrapped.LoadCaseNameInputs) if self.wrapped.LoadCaseNameInputs else None

    @property
    def file_inputs(self) -> 'List[_6298.MultiTimeSeriesDataInputFileOptions]':
        '''List[MultiTimeSeriesDataInputFileOptions]: 'FileInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FileInputs, constructor.new(_6298.MultiTimeSeriesDataInputFileOptions))
        return value

    @property
    def torque_inputs(self) -> 'List[_6304.TorqueInputOptions]':
        '''List[TorqueInputOptions]: 'TorqueInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueInputs, constructor.new(_6304.TorqueInputOptions))
        return value

    @property
    def speed_inputs(self) -> 'List[_6302.SpeedInputOptions]':
        '''List[SpeedInputOptions]: 'SpeedInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpeedInputs, constructor.new(_6302.SpeedInputOptions))
        return value

    @property
    def force_inputs(self) -> 'List[_6294.ForceInputOptions]':
        '''List[ForceInputOptions]: 'ForceInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ForceInputs, constructor.new(_6294.ForceInputOptions))
        return value

    @property
    def moment_inputs(self) -> 'List[_6297.MomentInputOptions]':
        '''List[MomentInputOptions]: 'MomentInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MomentInputs, constructor.new(_6297.MomentInputOptions))
        return value

    @property
    def boost_pressure_inputs(self) -> 'List[_6291.BoostPressureLoadCaseInputOptions]':
        '''List[BoostPressureLoadCaseInputOptions]: 'BoostPressureInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoostPressureInputs, constructor.new(_6291.BoostPressureLoadCaseInputOptions))
        return value

    @property
    def columns(self) -> 'List[_1441.ColumnTitle]':
        '''List[ColumnTitle]: 'Columns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Columns, constructor.new(_1441.ColumnTitle))
        return value
