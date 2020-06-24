'''_3868.py

ShaftHubConnectionModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1967
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2188
from mastapy.system_model.analyses_and_results.system_deflections import _2187
from mastapy.system_model.analyses_and_results.modal_analyses import _3916
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ShaftHubConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionModalAnalysis',)


class ShaftHubConnectionModalAnalysis(_3916.ConnectorModalAnalysis):
    '''ShaftHubConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionModalAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2187.ShaftHubConnectionSystemDeflection':
        '''ShaftHubConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.ShaftHubConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionModalAnalysis]':
        '''List[ShaftHubConnectionModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionModalAnalysis))
        return value
