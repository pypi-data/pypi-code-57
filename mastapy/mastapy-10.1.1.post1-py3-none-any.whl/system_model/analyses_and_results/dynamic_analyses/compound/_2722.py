'''_2722.py

BeltDriveCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1973
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3621
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2678
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'BeltDriveCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveCompoundDynamicAnalysis',)


class BeltDriveCompoundDynamicAnalysis(_2678.SpecialisedAssemblyCompoundDynamicAnalysis):
    '''BeltDriveCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1973.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1973.BeltDrive)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1973.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1973.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3621.BeltDriveDynamicAnalysis]':
        '''List[BeltDriveDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3621.BeltDriveDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_3621.BeltDriveDynamicAnalysis]':
        '''List[BeltDriveDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_3621.BeltDriveDynamicAnalysis))
        return value
