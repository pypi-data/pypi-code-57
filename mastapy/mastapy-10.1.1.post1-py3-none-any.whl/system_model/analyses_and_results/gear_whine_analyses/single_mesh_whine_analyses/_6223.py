'''_6223.py

ModalAnalysisForWhine
'''


from mastapy.system_model.analyses_and_results.modal_analyses import _5885
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_FOR_WHINE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ModalAnalysisForWhine')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisForWhine',)


class ModalAnalysisForWhine(_5885.ModalAnalysis):
    '''ModalAnalysisForWhine

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS_FOR_WHINE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisForWhine.TYPE'):
        super().__init__(instance_to_wrap)
