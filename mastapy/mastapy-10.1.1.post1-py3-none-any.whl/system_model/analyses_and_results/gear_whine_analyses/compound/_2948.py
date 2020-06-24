'''_2948.py

CylindricalGearMeshCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3781
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2957
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CylindricalGearMeshCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundGearWhineAnalysis',)


class CylindricalGearMeshCompoundGearWhineAnalysis(_2957.GearMeshCompoundGearWhineAnalysis):
    '''CylindricalGearMeshCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3781.CylindricalGearMeshGearWhineAnalysis]':
        '''List[CylindricalGearMeshGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3781.CylindricalGearMeshGearWhineAnalysis))
        return value

    @property
    def connection_gear_whine_analysis_load_cases(self) -> 'List[_3781.CylindricalGearMeshGearWhineAnalysis]':
        '''List[CylindricalGearMeshGearWhineAnalysis]: 'ConnectionGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionGearWhineAnalysisLoadCases, constructor.new(_3781.CylindricalGearMeshGearWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundGearWhineAnalysis]':
        '''List[CylindricalGearMeshCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCompoundGearWhineAnalysis))
        return value
