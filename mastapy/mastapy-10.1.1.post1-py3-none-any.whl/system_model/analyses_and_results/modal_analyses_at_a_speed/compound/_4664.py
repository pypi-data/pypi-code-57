'''_4664.py

RootAssemblyCompoundModalAnalysisAtASpeed
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4583
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'RootAssemblyCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundModalAnalysisAtASpeed',)


class RootAssemblyCompoundModalAnalysisAtASpeed(_4583.AssemblyCompoundModalAnalysisAtASpeed):
    '''RootAssemblyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
