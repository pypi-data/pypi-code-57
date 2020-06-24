'''_4136.py

SpringDamperHalfPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2019
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2196
from mastapy.system_model.analyses_and_results.power_flows import _4128
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SpringDamperHalfPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfPowerFlow',)


class SpringDamperHalfPowerFlow(_4128.CouplingHalfPowerFlow):
    '''SpringDamperHalfPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2019.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2019.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2196.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
