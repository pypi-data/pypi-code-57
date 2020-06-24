'''_4016.py

FaceGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6115
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4015, _4014, _4020
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'FaceGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetModalAnalysesAtSpeeds',)


class FaceGearSetModalAnalysesAtSpeeds(_4020.GearSetModalAnalysesAtSpeeds):
    '''FaceGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6115.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6115.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_modal_analyses_at_speeds(self) -> 'List[_4015.FaceGearModalAnalysesAtSpeeds]':
        '''List[FaceGearModalAnalysesAtSpeeds]: 'FaceGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsModalAnalysesAtSpeeds, constructor.new(_4015.FaceGearModalAnalysesAtSpeeds))
        return value

    @property
    def face_meshes_modal_analyses_at_speeds(self) -> 'List[_4014.FaceGearMeshModalAnalysesAtSpeeds]':
        '''List[FaceGearMeshModalAnalysesAtSpeeds]: 'FaceMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesModalAnalysesAtSpeeds, constructor.new(_4014.FaceGearMeshModalAnalysesAtSpeeds))
        return value
