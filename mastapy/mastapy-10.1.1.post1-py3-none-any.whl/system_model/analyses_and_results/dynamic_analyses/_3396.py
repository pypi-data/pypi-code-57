'''_3396.py

SynchroniserHalfDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2048
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2258
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3397
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SynchroniserHalfDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfDynamicAnalysis',)


class SynchroniserHalfDynamicAnalysis(_3397.SynchroniserPartDynamicAnalysis):
    '''SynchroniserHalfDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2048.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2048.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2258.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2258.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
