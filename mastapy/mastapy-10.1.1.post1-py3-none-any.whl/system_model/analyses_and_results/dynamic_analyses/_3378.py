'''_3378.py

ZerolBevelGearDynamicAnalysis
'''


from mastapy.system_model.part_model.gears import _2012
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2234
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3468
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ZerolBevelGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearDynamicAnalysis',)


class ZerolBevelGearDynamicAnalysis(_3468.BevelGearDynamicAnalysis):
    '''ZerolBevelGearDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2012.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2012.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2234.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2234.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
