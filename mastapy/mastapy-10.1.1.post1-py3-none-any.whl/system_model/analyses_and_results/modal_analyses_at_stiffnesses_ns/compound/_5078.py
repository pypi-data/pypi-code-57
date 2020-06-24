'''_5078.py

ConicalGearMeshCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5099
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'ConicalGearMeshCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshCompoundModalAnalysesAtStiffnesses',)


class ConicalGearMeshCompoundModalAnalysesAtStiffnesses(_5099.GearMeshCompoundModalAnalysesAtStiffnesses):
    '''ConicalGearMeshCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def planetaries(self) -> 'List[ConicalGearMeshCompoundModalAnalysesAtStiffnesses]':
        '''List[ConicalGearMeshCompoundModalAnalysesAtStiffnesses]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearMeshCompoundModalAnalysesAtStiffnesses))
        return value
