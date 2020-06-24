'''_3808.py

RollingRingConnectionModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1852
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6170
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3781
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'RollingRingConnectionModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionModalAnalysesAtStiffnesses',)


class RollingRingConnectionModalAnalysesAtStiffnesses(_3781.InterMountableComponentConnectionModalAnalysesAtStiffnesses):
    '''RollingRingConnectionModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1852.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1852.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6170.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6170.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionModalAnalysesAtStiffnesses]':
        '''List[RollingRingConnectionModalAnalysesAtStiffnesses]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionModalAnalysesAtStiffnesses))
        return value
