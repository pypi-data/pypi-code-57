'''_3357.py

CouplingConnectionCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3351
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CouplingConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundModalAnalysis',)


class CouplingConnectionCompoundModalAnalysis(_3351.InterMountableComponentConnectionCompoundModalAnalysis):
    '''CouplingConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
