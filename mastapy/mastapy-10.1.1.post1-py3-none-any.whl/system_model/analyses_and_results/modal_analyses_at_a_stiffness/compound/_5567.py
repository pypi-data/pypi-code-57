'''_5567.py

CVTPulleyCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _5619
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'CVTPulleyCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundModalAnalysisAtAStiffness',)


class CVTPulleyCompoundModalAnalysisAtAStiffness(_5619.PulleyCompoundModalAnalysisAtAStiffness):
    '''CVTPulleyCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
