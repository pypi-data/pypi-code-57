'''_3393.py

SpringDamperDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2036
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2252
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3385
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SpringDamperDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperDynamicAnalysis',)


class SpringDamperDynamicAnalysis(_3385.CouplingDynamicAnalysis):
    '''SpringDamperDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2036.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2036.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2252.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
