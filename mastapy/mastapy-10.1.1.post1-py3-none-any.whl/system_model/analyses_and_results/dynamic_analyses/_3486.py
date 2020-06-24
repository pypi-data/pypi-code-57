'''_3486.py

SpiralBevelGearDynamicAnalysis
'''


from mastapy.system_model.part_model.gears import _2002
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2365
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3468
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SpiralBevelGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearDynamicAnalysis',)


class SpiralBevelGearDynamicAnalysis(_3468.BevelGearDynamicAnalysis):
    '''SpiralBevelGearDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2002.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2002.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2365.SpiralBevelGearLoadCase':
        '''SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2365.SpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
