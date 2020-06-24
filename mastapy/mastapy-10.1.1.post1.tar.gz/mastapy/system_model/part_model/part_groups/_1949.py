'''_1949.py

DesignMeasurements
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets import _1763
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DESIGN_MEASUREMENTS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'DesignMeasurements')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignMeasurements',)


class DesignMeasurements(_1.APIBase):
    '''DesignMeasurements

    This is a mastapy class.
    '''

    TYPE = _DESIGN_MEASUREMENTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignMeasurements.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def component_connections(self) -> 'List[_1763.ComponentMeasurer]':
        '''List[ComponentMeasurer]: 'ComponentConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentConnections, constructor.new(_1763.ComponentMeasurer))
        return value
