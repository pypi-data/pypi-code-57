'''_4177.py

BoltPowerFlow
'''


from mastapy.system_model.part_model import _1910
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2266
from mastapy.system_model.analyses_and_results.power_flows import _4179
from mastapy._internal.python_net import python_net_import

_BOLT_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BoltPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltPowerFlow',)


class BoltPowerFlow(_4179.ComponentPowerFlow):
    '''BoltPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BOLT_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2266.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2266.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
