'''_4694.py

CylindricalGearMeshSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2244
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4705
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'CylindricalGearMeshSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshSteadyStateSynchronousResponse',)


class CylindricalGearMeshSteadyStateSynchronousResponse(_4705.GearMeshSteadyStateSynchronousResponse):
    '''CylindricalGearMeshSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2244.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshSteadyStateSynchronousResponse]':
        '''List[CylindricalGearMeshSteadyStateSynchronousResponse]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshSteadyStateSynchronousResponse))
        return value
