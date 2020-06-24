'''_4909.py

DutyCycleResultsForSingleShaft
'''


from mastapy.shafts import _42
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_RESULTS_FOR_SINGLE_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DutyCycleResultsForSingleShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleResultsForSingleShaft',)


class DutyCycleResultsForSingleShaft(_1.APIBase):
    '''DutyCycleResultsForSingleShaft

    This is a mastapy class.
    '''

    TYPE = _DUTY_CYCLE_RESULTS_FOR_SINGLE_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DutyCycleResultsForSingleShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def duty_cycle_results(self) -> '_42.ShaftDamageResults':
        '''ShaftDamageResults: 'DutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_42.ShaftDamageResults)(self.wrapped.DutyCycleResults) if self.wrapped.DutyCycleResults else None
