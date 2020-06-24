'''_3381.py

ClutchDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2034
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2238
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3385
from mastapy._internal.python_net import python_net_import

_CLUTCH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ClutchDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchDynamicAnalysis',)


class ClutchDynamicAnalysis(_3385.CouplingDynamicAnalysis):
    '''ClutchDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2034.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2238.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2238.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
