'''_2954.py

StraightBevelGearMeshCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1816
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3787
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2945
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'StraightBevelGearMeshCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshCompoundGearWhineAnalysis',)


class StraightBevelGearMeshCompoundGearWhineAnalysis(_2945.BevelGearMeshCompoundGearWhineAnalysis):
    '''StraightBevelGearMeshCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3787.StraightBevelGearMeshGearWhineAnalysis]':
        '''List[StraightBevelGearMeshGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3787.StraightBevelGearMeshGearWhineAnalysis))
        return value

    @property
    def connection_gear_whine_analysis_load_cases(self) -> 'List[_3787.StraightBevelGearMeshGearWhineAnalysis]':
        '''List[StraightBevelGearMeshGearWhineAnalysis]: 'ConnectionGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionGearWhineAnalysisLoadCases, constructor.new(_3787.StraightBevelGearMeshGearWhineAnalysis))
        return value
