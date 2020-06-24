'''_3718.py

HypoidGearDynamicAnalysis
'''


from mastapy.system_model.part_model.gears import _2002
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2336
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3703
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'HypoidGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearDynamicAnalysis',)


class HypoidGearDynamicAnalysis(_3703.AGMAGleasonConicalGearDynamicAnalysis):
    '''HypoidGearDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2002.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2002.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2336.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2336.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
