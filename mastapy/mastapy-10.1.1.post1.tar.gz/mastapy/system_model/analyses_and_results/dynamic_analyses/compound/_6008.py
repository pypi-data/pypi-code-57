'''_6008.py

SpecialisedAssemblyCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _5918
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'SpecialisedAssemblyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundDynamicAnalysis',)


class SpecialisedAssemblyCompoundDynamicAnalysis(_5918.AbstractAssemblyCompoundDynamicAnalysis):
    '''SpecialisedAssemblyCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
