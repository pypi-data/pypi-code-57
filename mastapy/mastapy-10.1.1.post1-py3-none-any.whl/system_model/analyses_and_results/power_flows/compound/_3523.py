'''_3523.py

FaceGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _1988
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3522, _3597, _3538
from mastapy.system_model.analyses_and_results.power_flows import _4174
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'FaceGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundPowerFlow',)


class FaceGearSetCompoundPowerFlow(_3538.GearSetCompoundPowerFlow):
    '''FaceGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1988.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1988.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_power_flow(self) -> 'List[_3522.FaceGearCompoundPowerFlow]':
        '''List[FaceGearCompoundPowerFlow]: 'FaceGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundPowerFlow, constructor.new(_3522.FaceGearCompoundPowerFlow))
        return value

    @property
    def face_meshes_compound_power_flow(self) -> 'List[_3597.FaceGearMeshCompoundPowerFlow]':
        '''List[FaceGearMeshCompoundPowerFlow]: 'FaceMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundPowerFlow, constructor.new(_3597.FaceGearMeshCompoundPowerFlow))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4174.FaceGearSetPowerFlow]':
        '''List[FaceGearSetPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4174.FaceGearSetPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_4174.FaceGearSetPowerFlow]':
        '''List[FaceGearSetPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_4174.FaceGearSetPowerFlow))
        return value
