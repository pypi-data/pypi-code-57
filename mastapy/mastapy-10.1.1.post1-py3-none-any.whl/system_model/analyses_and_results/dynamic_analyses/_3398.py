'''_3398.py

SynchroniserSleeveDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2049
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2262
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3397
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SynchroniserSleeveDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveDynamicAnalysis',)


class SynchroniserSleeveDynamicAnalysis(_3397.SynchroniserPartDynamicAnalysis):
    '''SynchroniserSleeveDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2049.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2049.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2262.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2262.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
