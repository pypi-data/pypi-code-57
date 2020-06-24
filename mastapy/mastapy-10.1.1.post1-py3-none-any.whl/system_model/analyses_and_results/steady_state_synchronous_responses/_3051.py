'''_3051.py

RootAssemblySteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _2015
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3062, _2969
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'RootAssemblySteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblySteadyStateSynchronousResponse',)


class RootAssemblySteadyStateSynchronousResponse(_2969.AssemblySteadyStateSynchronousResponse):
    '''RootAssemblySteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblySteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2015.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2015.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def steady_state_synchronous_response_inputs(self) -> '_3062.SteadyStateSynchronousResponse':
        '''SteadyStateSynchronousResponse: 'SteadyStateSynchronousResponseInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3062.SteadyStateSynchronousResponse)(self.wrapped.SteadyStateSynchronousResponseInputs) if self.wrapped.SteadyStateSynchronousResponseInputs else None
