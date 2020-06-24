'''_3266.py

FaceGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6115
from mastapy.gears.rating.face import _252
from mastapy.system_model.analyses_and_results.power_flows import _3265, _3264, _3270
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'FaceGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetPowerFlow',)


class FaceGearSetPowerFlow(_3270.GearSetPowerFlow):
    '''FaceGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetPowerFlow.TYPE'):
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
    def rating(self) -> '_252.FaceGearSetRating':
        '''FaceGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_252.FaceGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_252.FaceGearSetRating':
        '''FaceGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_252.FaceGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3265.FaceGearPowerFlow]':
        '''List[FaceGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3265.FaceGearPowerFlow))
        return value

    @property
    def face_gears_power_flow(self) -> 'List[_3265.FaceGearPowerFlow]':
        '''List[FaceGearPowerFlow]: 'FaceGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsPowerFlow, constructor.new(_3265.FaceGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3264.FaceGearMeshPowerFlow]':
        '''List[FaceGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3264.FaceGearMeshPowerFlow))
        return value

    @property
    def face_meshes_power_flow(self) -> 'List[_3264.FaceGearMeshPowerFlow]':
        '''List[FaceGearMeshPowerFlow]: 'FaceMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesPowerFlow, constructor.new(_3264.FaceGearMeshPowerFlow))
        return value
