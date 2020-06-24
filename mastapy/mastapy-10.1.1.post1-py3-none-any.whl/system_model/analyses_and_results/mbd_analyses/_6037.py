'''_6037.py

WormGearMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _1998
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2369
from mastapy.system_model.analyses_and_results.mbd_analyses import _5962
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'WormGearMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMultiBodyDynamicsAnalysis',)


class WormGearMultiBodyDynamicsAnalysis(_5962.GearMultiBodyDynamicsAnalysis):
    '''WormGearMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1998.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1998.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2369.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2369.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
