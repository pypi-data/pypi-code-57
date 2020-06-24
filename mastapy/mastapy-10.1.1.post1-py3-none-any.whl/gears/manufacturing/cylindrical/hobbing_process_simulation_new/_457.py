'''_457.py

HobbingProcessSimulationNew
'''


from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _452, _454, _455, _451,
    _453, _459, _470, _456
)
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_SIMULATION_NEW = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessSimulationNew')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessSimulationNew',)


class HobbingProcessSimulationNew(_470.ProcessSimulationNew['_456.HobbingProcessSimulationInput']):
    '''HobbingProcessSimulationNew

    This is a mastapy class.
    '''

    TYPE = _HOBBING_PROCESS_SIMULATION_NEW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HobbingProcessSimulationNew.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def hobbing_process_lead_calculation(self) -> '_452.HobbingProcessLeadCalculation':
        '''HobbingProcessLeadCalculation: 'HobbingProcessLeadCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_452.HobbingProcessLeadCalculation)(self.wrapped.HobbingProcessLeadCalculation) if self.wrapped.HobbingProcessLeadCalculation else None

    @property
    def hobbing_process_pitch_calculation(self) -> '_454.HobbingProcessPitchCalculation':
        '''HobbingProcessPitchCalculation: 'HobbingProcessPitchCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_454.HobbingProcessPitchCalculation)(self.wrapped.HobbingProcessPitchCalculation) if self.wrapped.HobbingProcessPitchCalculation else None

    @property
    def hobbing_process_profile_calculation(self) -> '_455.HobbingProcessProfileCalculation':
        '''HobbingProcessProfileCalculation: 'HobbingProcessProfileCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_455.HobbingProcessProfileCalculation)(self.wrapped.HobbingProcessProfileCalculation) if self.wrapped.HobbingProcessProfileCalculation else None

    @property
    def hobbing_process_gear_shape_calculation(self) -> '_451.HobbingProcessGearShape':
        '''HobbingProcessGearShape: 'HobbingProcessGearShapeCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_451.HobbingProcessGearShape)(self.wrapped.HobbingProcessGearShapeCalculation) if self.wrapped.HobbingProcessGearShapeCalculation else None

    @property
    def hobbing_process_mark_on_shaft_calculation(self) -> '_453.HobbingProcessMarkOnShaft':
        '''HobbingProcessMarkOnShaft: 'HobbingProcessMarkOnShaftCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_453.HobbingProcessMarkOnShaft)(self.wrapped.HobbingProcessMarkOnShaftCalculation) if self.wrapped.HobbingProcessMarkOnShaftCalculation else None

    @property
    def hobbing_process_total_modification(self) -> '_459.HobbingProcessTotalModificationCalculation':
        '''HobbingProcessTotalModificationCalculation: 'HobbingProcessTotalModification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_459.HobbingProcessTotalModificationCalculation)(self.wrapped.HobbingProcessTotalModification) if self.wrapped.HobbingProcessTotalModification else None
