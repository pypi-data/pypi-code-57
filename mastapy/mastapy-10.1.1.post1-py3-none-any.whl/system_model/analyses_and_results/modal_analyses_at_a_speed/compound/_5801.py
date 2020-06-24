'''_5801.py

CouplingHalfCompoundModalAnalysisAtASpeed
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5835
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'CouplingHalfCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundModalAnalysisAtASpeed',)


class CouplingHalfCompoundModalAnalysisAtASpeed(_5835.MountableComponentCompoundModalAnalysisAtASpeed):
    '''CouplingHalfCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
