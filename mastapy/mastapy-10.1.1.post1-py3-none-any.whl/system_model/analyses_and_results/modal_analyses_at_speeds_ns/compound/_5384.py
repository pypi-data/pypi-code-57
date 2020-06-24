'''_5384.py

StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1814
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5265
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5304
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds',)


class StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds(_5304.BevelGearMeshCompoundModalAnalysesAtSpeeds):
    '''StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5265.StraightBevelDiffGearMeshModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearMeshModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5265.StraightBevelDiffGearMeshModalAnalysesAtSpeeds))
        return value

    @property
    def connection_modal_analyses_at_speeds_load_cases(self) -> 'List[_5265.StraightBevelDiffGearMeshModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearMeshModalAnalysesAtSpeeds]: 'ConnectionModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtSpeedsLoadCases, constructor.new(_5265.StraightBevelDiffGearMeshModalAnalysesAtSpeeds))
        return value
