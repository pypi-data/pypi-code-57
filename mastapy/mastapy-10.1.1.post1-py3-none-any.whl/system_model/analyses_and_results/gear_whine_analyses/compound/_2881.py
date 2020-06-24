'''_2881.py

CylindricalGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2880, _2948, _2884
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3832
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CylindricalGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundGearWhineAnalysis',)


class CylindricalGearSetCompoundGearWhineAnalysis(_2884.GearSetCompoundGearWhineAnalysis):
    '''CylindricalGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_gear_whine_analysis(self) -> 'List[_2880.CylindricalGearCompoundGearWhineAnalysis]':
        '''List[CylindricalGearCompoundGearWhineAnalysis]: 'CylindricalGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundGearWhineAnalysis, constructor.new(_2880.CylindricalGearCompoundGearWhineAnalysis))
        return value

    @property
    def cylindrical_meshes_compound_gear_whine_analysis(self) -> 'List[_2948.CylindricalGearMeshCompoundGearWhineAnalysis]':
        '''List[CylindricalGearMeshCompoundGearWhineAnalysis]: 'CylindricalMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundGearWhineAnalysis, constructor.new(_2948.CylindricalGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3832.CylindricalGearSetGearWhineAnalysis]':
        '''List[CylindricalGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3832.CylindricalGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_3832.CylindricalGearSetGearWhineAnalysis]':
        '''List[CylindricalGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_3832.CylindricalGearSetGearWhineAnalysis))
        return value
