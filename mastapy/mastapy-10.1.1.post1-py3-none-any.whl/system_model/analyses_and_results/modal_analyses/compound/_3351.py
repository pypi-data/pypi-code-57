'''_3351.py

InterMountableComponentConnectionCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3350
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'InterMountableComponentConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('InterMountableComponentConnectionCompoundModalAnalysis',)


class InterMountableComponentConnectionCompoundModalAnalysis(_3350.ConnectionCompoundModalAnalysis):
    '''InterMountableComponentConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'InterMountableComponentConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
