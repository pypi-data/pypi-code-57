'''_2677.py

RootAssemblyCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2666
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'RootAssemblyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundDynamicAnalysis',)


class RootAssemblyCompoundDynamicAnalysis(_2666.AssemblyCompoundDynamicAnalysis):
    '''RootAssemblyCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
