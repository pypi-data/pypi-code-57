'''_4220.py

BeltDriveModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _2111
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6056
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4304
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'BeltDriveModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveModalAnalysisAtAStiffness',)


class BeltDriveModalAnalysisAtAStiffness(_4304.SpecialisedAssemblyModalAnalysisAtAStiffness):
    '''BeltDriveModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2111.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6056.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6056.BeltDriveLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
