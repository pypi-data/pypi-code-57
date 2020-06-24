'''_689.py

ProcessPitchCalculation
'''


from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _661
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PROCESS_PITCH_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessPitchCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessPitchCalculation',)


class ProcessPitchCalculation(_1.APIBase):
    '''ProcessPitchCalculation

    This is a mastapy class.
    '''

    TYPE = _PROCESS_PITCH_CALCULATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessPitchCalculation.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def right_flank_accuracy_calculation(self) -> '_661.CalculatePitchDeviationAccuracy':
        '''CalculatePitchDeviationAccuracy: 'RightFlankAccuracyCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_661.CalculatePitchDeviationAccuracy)(self.wrapped.RightFlankAccuracyCalculation) if self.wrapped.RightFlankAccuracyCalculation else None

    @property
    def left_flank_accuracy_calculation(self) -> '_661.CalculatePitchDeviationAccuracy':
        '''CalculatePitchDeviationAccuracy: 'LeftFlankAccuracyCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_661.CalculatePitchDeviationAccuracy)(self.wrapped.LeftFlankAccuracyCalculation) if self.wrapped.LeftFlankAccuracyCalculation else None
