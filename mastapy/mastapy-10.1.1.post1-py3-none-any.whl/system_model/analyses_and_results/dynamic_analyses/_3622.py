'''_3622.py

ClutchDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _1988
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2173
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3626
from mastapy._internal.python_net import python_net_import

_CLUTCH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ClutchDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchDynamicAnalysis',)


class ClutchDynamicAnalysis(_3626.CouplingDynamicAnalysis):
    '''ClutchDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1988.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2173.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
