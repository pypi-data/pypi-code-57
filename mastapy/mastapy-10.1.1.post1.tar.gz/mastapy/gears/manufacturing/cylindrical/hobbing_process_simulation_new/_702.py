'''_702.py

ProcessSimulationNew
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _698, _700, _699, _697,
    _704, _701
)
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PROCESS_SIMULATION_NEW = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessSimulationNew')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessSimulationNew',)


T = TypeVar('T', bound='_701.ProcessSimulationInput')


class ProcessSimulationNew(_1.APIBase, Generic[T]):
    '''ProcessSimulationNew

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _PROCESS_SIMULATION_NEW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessSimulationNew.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def achieved_iso132811995e_quality_grade(self) -> 'float':
        '''float: 'AchievedISO132811995EQualityGrade' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AchievedISO132811995EQualityGrade

    @property
    def achieved_ansiagma20151a01_quality_grade(self) -> 'float':
        '''float: 'AchievedANSIAGMA20151A01QualityGrade' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AchievedANSIAGMA20151A01QualityGrade

    @property
    def input(self) -> 'T':
        '''T: 'Input' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.wrapped.Input) if self.wrapped.Input else None

    @property
    def lead_calculation(self) -> '_698.ProcessLeadCalculation':
        '''ProcessLeadCalculation: 'LeadCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_698.ProcessLeadCalculation)(self.wrapped.LeadCalculation) if self.wrapped.LeadCalculation else None

    @property
    def profile_calculation(self) -> '_700.ProcessProfileCalculation':
        '''ProcessProfileCalculation: 'ProfileCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_700.ProcessProfileCalculation)(self.wrapped.ProfileCalculation) if self.wrapped.ProfileCalculation else None

    @property
    def pitch_calculation(self) -> '_699.ProcessPitchCalculation':
        '''ProcessPitchCalculation: 'PitchCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_699.ProcessPitchCalculation)(self.wrapped.PitchCalculation) if self.wrapped.PitchCalculation else None

    @property
    def gear_tooth_shape_calculation(self) -> '_697.ProcessGearShape':
        '''ProcessGearShape: 'GearToothShapeCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_697.ProcessGearShape)(self.wrapped.GearToothShapeCalculation) if self.wrapped.GearToothShapeCalculation else None

    @property
    def total_modification_calculation(self) -> '_704.ProcessTotalModificationCalculation':
        '''ProcessTotalModificationCalculation: 'TotalModificationCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_704.ProcessTotalModificationCalculation)(self.wrapped.TotalModificationCalculation) if self.wrapped.TotalModificationCalculation else None
