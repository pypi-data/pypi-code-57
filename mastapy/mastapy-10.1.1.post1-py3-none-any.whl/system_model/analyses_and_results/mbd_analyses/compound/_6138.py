'''_6138.py

SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1966
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6136, _6137, _6064
from mastapy.system_model.analyses_and_results.mbd_analyses import _6011
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis',)


class SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis(_6064.BevelGearSetCompoundMultiBodyDynamicsAnalysis):
    '''SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1966.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1966.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_6136.SpiralBevelGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearCompoundMultiBodyDynamicsAnalysis]: 'SpiralBevelGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_6136.SpiralBevelGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_6137.SpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis]: 'SpiralBevelMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_6137.SpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6011.SpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6011.SpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_6011.SpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_6011.SpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value
