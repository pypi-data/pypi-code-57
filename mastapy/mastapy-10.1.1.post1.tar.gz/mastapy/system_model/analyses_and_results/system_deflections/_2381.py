'''_2381.py

ObservedPinStiffnessReporter
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_OBSERVED_PIN_STIFFNESS_REPORTER = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ObservedPinStiffnessReporter')


__docformat__ = 'restructuredtext en'
__all__ = ('ObservedPinStiffnessReporter',)


class ObservedPinStiffnessReporter(_1.APIBase):
    '''ObservedPinStiffnessReporter

    This is a mastapy class.
    '''

    TYPE = _OBSERVED_PIN_STIFFNESS_REPORTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ObservedPinStiffnessReporter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pin_assembly_stiffness_observed_at_planets(self) -> 'float':
        '''float: 'PinAssemblyStiffnessObservedAtPlanets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinAssemblyStiffnessObservedAtPlanets
