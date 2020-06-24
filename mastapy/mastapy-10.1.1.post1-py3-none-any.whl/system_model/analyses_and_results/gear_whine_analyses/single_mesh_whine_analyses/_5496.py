'''_5496.py

ShaftHubConnectionSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2132
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6173
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5442
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ShaftHubConnectionSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionSingleMeshWhineAnalysis',)


class ShaftHubConnectionSingleMeshWhineAnalysis(_5442.ConnectorSingleMeshWhineAnalysis):
    '''ShaftHubConnectionSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2132.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6173.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6173.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionSingleMeshWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionSingleMeshWhineAnalysis))
        return value
