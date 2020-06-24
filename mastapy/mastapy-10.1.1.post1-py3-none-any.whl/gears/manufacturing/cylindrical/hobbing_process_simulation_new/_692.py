'''_692.py

ProcessSimulationInput
'''


from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _664, _659, _697, _666,
    _665
)
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PROCESS_SIMULATION_INPUT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessSimulationInput')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessSimulationInput',)


class ProcessSimulationInput(_1.APIBase):
    '''ProcessSimulationInput

    This is a mastapy class.
    '''

    TYPE = _PROCESS_SIMULATION_INPUT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessSimulationInput.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def start_height_above_the_gear_center(self) -> 'float':
        '''float: 'StartHeightAboveTheGearCenter' is the original name of this property.'''

        return self.wrapped.StartHeightAboveTheGearCenter

    @start_height_above_the_gear_center.setter
    def start_height_above_the_gear_center(self, value: 'float'):
        self.wrapped.StartHeightAboveTheGearCenter = float(value) if value else 0.0

    @property
    def feed(self) -> 'float':
        '''float: 'Feed' is the original name of this property.'''

        return self.wrapped.Feed

    @feed.setter
    def feed(self, value: 'float'):
        self.wrapped.Feed = float(value) if value else 0.0

    @property
    def centre_distance_offset_specification_method(self) -> '_664.CentreDistanceOffsetMethod':
        '''CentreDistanceOffsetMethod: 'CentreDistanceOffsetSpecificationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CentreDistanceOffsetSpecificationMethod)
        return constructor.new(_664.CentreDistanceOffsetMethod)(value) if value else None

    @centre_distance_offset_specification_method.setter
    def centre_distance_offset_specification_method(self, value: '_664.CentreDistanceOffsetMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CentreDistanceOffsetSpecificationMethod = value

    @property
    def centre_distance_offset(self) -> 'float':
        '''float: 'CentreDistanceOffset' is the original name of this property.'''

        return self.wrapped.CentreDistanceOffset

    @centre_distance_offset.setter
    def centre_distance_offset(self, value: 'float'):
        self.wrapped.CentreDistanceOffset = float(value) if value else 0.0

    @property
    def gear_design_lead_crown_modification(self) -> 'float':
        '''float: 'GearDesignLeadCrownModification' is the original name of this property.'''

        return self.wrapped.GearDesignLeadCrownModification

    @gear_design_lead_crown_modification.setter
    def gear_design_lead_crown_modification(self, value: 'float'):
        self.wrapped.GearDesignLeadCrownModification = float(value) if value else 0.0

    @property
    def gear_designed_lead_crown_length(self) -> 'float':
        '''float: 'GearDesignedLeadCrownLength' is the original name of this property.'''

        return self.wrapped.GearDesignedLeadCrownLength

    @gear_designed_lead_crown_length.setter
    def gear_designed_lead_crown_length(self, value: 'float'):
        self.wrapped.GearDesignedLeadCrownLength = float(value) if value else 0.0

    @property
    def analysis_setting(self) -> '_659.AnalysisMethod':
        '''AnalysisMethod: 'AnalysisSetting' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AnalysisSetting)
        return constructor.new(_659.AnalysisMethod)(value) if value else None

    @analysis_setting.setter
    def analysis_setting(self, value: '_659.AnalysisMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AnalysisSetting = value

    @property
    def shaft_angle_offset(self) -> 'float':
        '''float: 'ShaftAngleOffset' is the original name of this property.'''

        return self.wrapped.ShaftAngleOffset

    @shaft_angle_offset.setter
    def shaft_angle_offset(self, value: 'float'):
        self.wrapped.ShaftAngleOffset = float(value) if value else 0.0

    @property
    def tooth_index(self) -> 'int':
        '''int: 'ToothIndex' is the original name of this property.'''

        return self.wrapped.ToothIndex

    @tooth_index.setter
    def tooth_index(self, value: 'int'):
        self.wrapped.ToothIndex = int(value) if value else 0

    @property
    def cutter_mounting_error(self) -> '_697.RackMountingError':
        '''RackMountingError: 'CutterMountingError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_697.RackMountingError)(self.wrapped.CutterMountingError) if self.wrapped.CutterMountingError else None

    @property
    def gear_mounting_error(self) -> '_666.GearMountingError':
        '''GearMountingError: 'GearMountingError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_666.GearMountingError)(self.wrapped.GearMountingError) if self.wrapped.GearMountingError else None

    @property
    def cutter_head_slide_error(self) -> '_665.CutterHeadSlideError':
        '''CutterHeadSlideError: 'CutterHeadSlideError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_665.CutterHeadSlideError)(self.wrapped.CutterHeadSlideError) if self.wrapped.CutterHeadSlideError else None
