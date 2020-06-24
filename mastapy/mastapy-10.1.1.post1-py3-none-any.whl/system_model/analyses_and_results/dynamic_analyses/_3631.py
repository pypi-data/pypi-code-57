'''_3631.py

ShaftHubConnectionDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1967
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2188
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3679
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ShaftHubConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionDynamicAnalysis',)


class ShaftHubConnectionDynamicAnalysis(_3679.ConnectorDynamicAnalysis):
    '''ShaftHubConnectionDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1967.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1967.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2188.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2188.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionDynamicAnalysis]':
        '''List[ShaftHubConnectionDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionDynamicAnalysis))
        return value
