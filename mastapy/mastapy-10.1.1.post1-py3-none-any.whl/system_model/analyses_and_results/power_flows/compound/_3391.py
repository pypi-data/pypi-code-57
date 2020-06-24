'''_3391.py

FaceGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3389, _3390, _3395
from mastapy.system_model.analyses_and_results.power_flows import _3266
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'FaceGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundPowerFlow',)


class FaceGearSetCompoundPowerFlow(_3395.GearSetCompoundPowerFlow):
    '''FaceGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_power_flow(self) -> 'List[_3389.FaceGearCompoundPowerFlow]':
        '''List[FaceGearCompoundPowerFlow]: 'FaceGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundPowerFlow, constructor.new(_3389.FaceGearCompoundPowerFlow))
        return value

    @property
    def face_meshes_compound_power_flow(self) -> 'List[_3390.FaceGearMeshCompoundPowerFlow]':
        '''List[FaceGearMeshCompoundPowerFlow]: 'FaceMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundPowerFlow, constructor.new(_3390.FaceGearMeshCompoundPowerFlow))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3266.FaceGearSetPowerFlow]':
        '''List[FaceGearSetPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3266.FaceGearSetPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3266.FaceGearSetPowerFlow]':
        '''List[FaceGearSetPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3266.FaceGearSetPowerFlow))
        return value
