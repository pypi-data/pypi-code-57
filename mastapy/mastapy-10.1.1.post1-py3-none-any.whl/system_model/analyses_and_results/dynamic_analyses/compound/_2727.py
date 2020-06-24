'''_2727.py

CouplingCompoundDynamicAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2678
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'CouplingCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundDynamicAnalysis',)


class CouplingCompoundDynamicAnalysis(_2678.SpecialisedAssemblyCompoundDynamicAnalysis):
    '''CouplingCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
