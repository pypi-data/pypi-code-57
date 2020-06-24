'''_4908.py

DutyCycleResultsForSingleBearing
'''


from mastapy.bearings.bearing_results import _1521
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_RESULTS_FOR_SINGLE_BEARING = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DutyCycleResultsForSingleBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleResultsForSingleBearing',)


class DutyCycleResultsForSingleBearing(_1.APIBase):
    '''DutyCycleResultsForSingleBearing

    This is a mastapy class.
    '''

    TYPE = _DUTY_CYCLE_RESULTS_FOR_SINGLE_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DutyCycleResultsForSingleBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def duty_cycle_results(self) -> '_1521.LoadedBearingDutyCycle':
        '''LoadedBearingDutyCycle: 'DutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1521.LoadedBearingDutyCycle)(self.wrapped.DutyCycleResults) if self.wrapped.DutyCycleResults else None
