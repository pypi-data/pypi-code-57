'''_4138.py

SynchroniserHalfPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows import _4152, _4139
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2024
from mastapy.system_model.analyses_and_results.static_loads import _2200
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SynchroniserHalfPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfPowerFlow',)


class SynchroniserHalfPowerFlow(_4139.SynchroniserPartPowerFlow):
    '''SynchroniserHalfPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def clutch_connection(self) -> '_4152.ClutchConnectionPowerFlow':
        '''ClutchConnectionPowerFlow: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4152.ClutchConnectionPowerFlow)(self.wrapped.ClutchConnection) if self.wrapped.ClutchConnection else None

    @property
    def component_design(self) -> '_2024.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2024.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2200.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
