'''_2642.py

BeltDriveSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _1973
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2172
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2959
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'BeltDriveSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveSteadyStateSynchronousResponseOnAShaft',)


class BeltDriveSteadyStateSynchronousResponseOnAShaft(_2959.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft):
    '''BeltDriveSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1973.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1973.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2172.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2172.BeltDriveLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
