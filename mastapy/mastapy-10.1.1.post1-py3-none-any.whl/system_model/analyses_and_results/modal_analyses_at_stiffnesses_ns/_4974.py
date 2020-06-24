'''_4974.py

FaceGearSetModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _1978
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2312
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4973, _4972, _4978
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'FaceGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetModalAnalysesAtStiffnesses',)


class FaceGearSetModalAnalysesAtStiffnesses(_4978.GearSetModalAnalysesAtStiffnesses):
    '''FaceGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1978.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2312.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2312.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_modal_analyses_at_stiffnesses(self) -> 'List[_4973.FaceGearModalAnalysesAtStiffnesses]':
        '''List[FaceGearModalAnalysesAtStiffnesses]: 'FaceGearsModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsModalAnalysesAtStiffnesses, constructor.new(_4973.FaceGearModalAnalysesAtStiffnesses))
        return value

    @property
    def face_meshes_modal_analyses_at_stiffnesses(self) -> 'List[_4972.FaceGearMeshModalAnalysesAtStiffnesses]':
        '''List[FaceGearMeshModalAnalysesAtStiffnesses]: 'FaceMeshesModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesModalAnalysesAtStiffnesses, constructor.new(_4972.FaceGearMeshModalAnalysesAtStiffnesses))
        return value
