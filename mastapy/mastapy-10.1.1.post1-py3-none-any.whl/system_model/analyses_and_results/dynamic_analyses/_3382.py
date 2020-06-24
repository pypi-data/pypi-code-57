'''_3382.py

ClutchHalfDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2039
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2239
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3386
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ClutchHalfDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfDynamicAnalysis',)


class ClutchHalfDynamicAnalysis(_3386.CouplingHalfDynamicAnalysis):
    '''ClutchHalfDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2039.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2039.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2239.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
