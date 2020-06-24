'''_5835.py

MountableComponentCompoundModalAnalysisAtASpeed
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5787
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'MountableComponentCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundModalAnalysisAtASpeed',)


class MountableComponentCompoundModalAnalysisAtASpeed(_5787.ComponentCompoundModalAnalysisAtASpeed):
    '''MountableComponentCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
