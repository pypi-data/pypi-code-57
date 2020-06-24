'''_5057.py

PlanetCarrierMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _2010
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6162
from mastapy.system_model.analyses_and_results.mbd_analyses import _5048
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PlanetCarrierMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierMultiBodyDynamicsAnalysis',)


class PlanetCarrierMultiBodyDynamicsAnalysis(_5048.MountableComponentMultiBodyDynamicsAnalysis):
    '''PlanetCarrierMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2010.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2010.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6162.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6162.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
