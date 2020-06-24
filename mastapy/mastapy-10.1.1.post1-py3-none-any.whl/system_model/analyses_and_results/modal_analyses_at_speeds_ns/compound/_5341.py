'''_5341.py

GearMeshCompoundModalAnalysesAtSpeeds
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5348
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'GearMeshCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundModalAnalysesAtSpeeds',)


class GearMeshCompoundModalAnalysesAtSpeeds(_5348.InterMountableComponentConnectionCompoundModalAnalysesAtSpeeds):
    '''GearMeshCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
