'''_6165.py

ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1983
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6163, _6164, _6064
from mastapy.system_model.analyses_and_results.mbd_analyses import _6041
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis',)


class ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis(_6064.BevelGearSetCompoundMultiBodyDynamicsAnalysis):
    '''ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_6163.ZerolBevelGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearCompoundMultiBodyDynamicsAnalysis]: 'ZerolBevelGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_6163.ZerolBevelGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_6164.ZerolBevelGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMeshCompoundMultiBodyDynamicsAnalysis]: 'ZerolBevelMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_6164.ZerolBevelGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6041.ZerolBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6041.ZerolBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_6041.ZerolBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_6041.ZerolBevelGearSetMultiBodyDynamicsAnalysis))
        return value
