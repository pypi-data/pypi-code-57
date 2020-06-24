'''_4352.py

PlanetCarrierSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _1932
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2293
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4349
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'PlanetCarrierSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierSingleMeshWhineAnalysis',)


class PlanetCarrierSingleMeshWhineAnalysis(_4349.MountableComponentSingleMeshWhineAnalysis):
    '''PlanetCarrierSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2293.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2293.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
