'''_5184.py

PartCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6492
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'PartCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundMultiBodyDynamicsAnalysis',)


class PartCompoundMultiBodyDynamicsAnalysis(_6492.PartCompoundAnalysis):
    '''PartCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
