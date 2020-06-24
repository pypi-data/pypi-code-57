'''_4199.py

ShaftPowerFlow
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.analyses_and_results.static_loads import _2306
from mastapy.system_model.analyses_and_results.power_flows import _4175
from mastapy._internal.python_net import python_net_import

_SHAFT_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ShaftPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftPowerFlow',)


class ShaftPowerFlow(_4175.AbstractShaftOrHousingPowerFlow):
    '''ShaftPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SHAFT_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pin_tangential_oscillation_frequency(self) -> 'float':
        '''float: 'PinTangentialOscillationFrequency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinTangentialOscillationFrequency

    @property
    def component_design(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2306.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2306.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
