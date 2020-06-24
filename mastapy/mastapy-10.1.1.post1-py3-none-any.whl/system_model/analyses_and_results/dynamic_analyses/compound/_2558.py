'''_2558.py

FaceGearSetCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2557, _2632, _2573
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3702
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'FaceGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundDynamicAnalysis',)


class FaceGearSetCompoundDynamicAnalysis(_2573.GearSetCompoundDynamicAnalysis):
    '''FaceGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1981.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1981.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_dynamic_analysis(self) -> 'List[_2557.FaceGearCompoundDynamicAnalysis]':
        '''List[FaceGearCompoundDynamicAnalysis]: 'FaceGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundDynamicAnalysis, constructor.new(_2557.FaceGearCompoundDynamicAnalysis))
        return value

    @property
    def face_meshes_compound_dynamic_analysis(self) -> 'List[_2632.FaceGearMeshCompoundDynamicAnalysis]':
        '''List[FaceGearMeshCompoundDynamicAnalysis]: 'FaceMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundDynamicAnalysis, constructor.new(_2632.FaceGearMeshCompoundDynamicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3702.FaceGearSetDynamicAnalysis]':
        '''List[FaceGearSetDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3702.FaceGearSetDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_3702.FaceGearSetDynamicAnalysis]':
        '''List[FaceGearSetDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_3702.FaceGearSetDynamicAnalysis))
        return value
