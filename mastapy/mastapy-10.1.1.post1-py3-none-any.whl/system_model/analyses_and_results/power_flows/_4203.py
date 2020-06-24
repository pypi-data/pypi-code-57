'''_4203.py

FaceGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _1978
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2312
from mastapy.gears.rating.face import _396
from mastapy.system_model.analyses_and_results.power_flows import _4202, _4159, _4218
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'FaceGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetPowerFlow',)


class FaceGearSetPowerFlow(_4218.GearSetPowerFlow):
    '''FaceGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetPowerFlow.TYPE'):
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
    def rating(self) -> '_396.FaceGearSetRating':
        '''FaceGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_396.FaceGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_396.FaceGearSetRating':
        '''FaceGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_396.FaceGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def face_gears_power_flow(self) -> 'List[_4202.FaceGearPowerFlow]':
        '''List[FaceGearPowerFlow]: 'FaceGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsPowerFlow, constructor.new(_4202.FaceGearPowerFlow))
        return value

    @property
    def face_meshes_power_flow(self) -> 'List[_4159.FaceGearMeshPowerFlow]':
        '''List[FaceGearMeshPowerFlow]: 'FaceMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesPowerFlow, constructor.new(_4159.FaceGearMeshPowerFlow))
        return value
