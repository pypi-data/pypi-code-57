'''_3694.py

RootAssemblyDynamicAnalysis
'''


from mastapy.system_model.part_model import _1935
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _4899, _3683
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'RootAssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyDynamicAnalysis',)


class RootAssemblyDynamicAnalysis(_3683.AssemblyDynamicAnalysis):
    '''RootAssemblyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1935.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1935.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def dynamic_analysis_inputs(self) -> '_4899.DynamicAnalysis':
        '''DynamicAnalysis: 'DynamicAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4899.DynamicAnalysis)(self.wrapped.DynamicAnalysisInputs) if self.wrapped.DynamicAnalysisInputs else None
