'''_691.py

ProcessProfileCalculation
'''


from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _662
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PROCESS_PROFILE_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessProfileCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessProfileCalculation',)


class ProcessProfileCalculation(_1.APIBase):
    '''ProcessProfileCalculation

    This is a mastapy class.
    '''

    TYPE = _PROCESS_PROFILE_CALCULATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessProfileCalculation.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def right_flank_accuracy_calculation(self) -> '_662.CalculateProfileDeviationAccuracy':
        '''CalculateProfileDeviationAccuracy: 'RightFlankAccuracyCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_662.CalculateProfileDeviationAccuracy)(self.wrapped.RightFlankAccuracyCalculation) if self.wrapped.RightFlankAccuracyCalculation else None

    @property
    def left_flank_accuracy_calculation(self) -> '_662.CalculateProfileDeviationAccuracy':
        '''CalculateProfileDeviationAccuracy: 'LeftFlankAccuracyCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_662.CalculateProfileDeviationAccuracy)(self.wrapped.LeftFlankAccuracyCalculation) if self.wrapped.LeftFlankAccuracyCalculation else None
