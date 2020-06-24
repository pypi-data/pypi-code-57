'''_4681.py

ConceptGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2308
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4682, _4680, _4706
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ConceptGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetSteadyStateSynchronousResponse',)


class ConceptGearSetSteadyStateSynchronousResponse(_4706.GearSetSteadyStateSynchronousResponse):
    '''ConceptGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1977.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2308.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2308.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_steady_state_synchronous_response(self) -> 'List[_4682.ConceptGearSteadyStateSynchronousResponse]':
        '''List[ConceptGearSteadyStateSynchronousResponse]: 'ConceptGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsSteadyStateSynchronousResponse, constructor.new(_4682.ConceptGearSteadyStateSynchronousResponse))
        return value

    @property
    def concept_meshes_steady_state_synchronous_response(self) -> 'List[_4680.ConceptGearMeshSteadyStateSynchronousResponse]':
        '''List[ConceptGearMeshSteadyStateSynchronousResponse]: 'ConceptMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesSteadyStateSynchronousResponse, constructor.new(_4680.ConceptGearMeshSteadyStateSynchronousResponse))
        return value
