'''_3325.py

BeltDriveCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2029
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3857
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3281
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'BeltDriveCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveCompoundModalAnalysis',)


class BeltDriveCompoundModalAnalysis(_3281.SpecialisedAssemblyCompoundModalAnalysis):
    '''BeltDriveCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2029.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2029.BeltDrive)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2029.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2029.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3857.BeltDriveModalAnalysis]':
        '''List[BeltDriveModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3857.BeltDriveModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3857.BeltDriveModalAnalysis]':
        '''List[BeltDriveModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3857.BeltDriveModalAnalysis))
        return value
