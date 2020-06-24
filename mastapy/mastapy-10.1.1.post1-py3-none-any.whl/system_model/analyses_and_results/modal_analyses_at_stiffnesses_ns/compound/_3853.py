'''_3853.py

BeltDriveCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2111
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3729
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3935
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'BeltDriveCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveCompoundModalAnalysesAtStiffnesses',)


class BeltDriveCompoundModalAnalysesAtStiffnesses(_3935.SpecialisedAssemblyCompoundModalAnalysesAtStiffnesses):
    '''BeltDriveCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2111.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.BeltDrive)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2111.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3729.BeltDriveModalAnalysesAtStiffnesses]':
        '''List[BeltDriveModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3729.BeltDriveModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3729.BeltDriveModalAnalysesAtStiffnesses]':
        '''List[BeltDriveModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_3729.BeltDriveModalAnalysesAtStiffnesses))
        return value
