'''_5527.py

AbstractAssemblyCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _5616
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'AbstractAssemblyCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyCompoundModalAnalysisAtAStiffness',)


class AbstractAssemblyCompoundModalAnalysisAtAStiffness(_5616.PartCompoundModalAnalysisAtAStiffness):
    '''AbstractAssemblyCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractAssemblyCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
