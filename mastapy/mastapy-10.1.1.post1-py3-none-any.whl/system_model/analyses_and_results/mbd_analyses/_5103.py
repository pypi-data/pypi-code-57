'''_5103.py

ZerolBevelGearMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _2092
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6212
from mastapy.system_model.analyses_and_results.mbd_analyses import _4983
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ZerolBevelGearMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMultiBodyDynamicsAnalysis',)


class ZerolBevelGearMultiBodyDynamicsAnalysis(_4983.BevelGearMultiBodyDynamicsAnalysis):
    '''ZerolBevelGearMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2092.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2092.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6212.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6212.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
