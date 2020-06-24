'''_6262.py

DataFromJMAGPerSpeed
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import _6261
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DATA_FROM_JMAG_PER_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'DataFromJMAGPerSpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('DataFromJMAGPerSpeed',)


class DataFromJMAGPerSpeed(_1.APIBase):
    '''DataFromJMAGPerSpeed

    This is a mastapy class.
    '''

    TYPE = _DATA_FROM_JMAG_PER_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DataFromJMAGPerSpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def speed(self) -> 'float':
        '''float: 'Speed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Speed

    @property
    def torque_selector(self) -> 'list_with_selected_item.ListWithSelectedItem_float':
        '''list_with_selected_item.ListWithSelectedItem_float: 'TorqueSelector' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_float)(self.wrapped.TorqueSelector) if self.wrapped.TorqueSelector else None

    @torque_selector.setter
    def torque_selector(self, value: 'list_with_selected_item.ListWithSelectedItem_float.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_float.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TorqueSelector = value

    @property
    def torque(self) -> 'float':
        '''float: 'Torque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Torque

    @property
    def include(self) -> 'bool':
        '''bool: 'Include' is the original name of this property.'''

        return self.wrapped.Include

    @include.setter
    def include(self, value: 'bool'):
        self.wrapped.Include = bool(value) if value else False

    @property
    def data_per_mean_torque(self) -> 'List[_6261.DataFromJMAGPerMeanTorque]':
        '''List[DataFromJMAGPerMeanTorque]: 'DataPerMeanTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DataPerMeanTorque, constructor.new(_6261.DataFromJMAGPerMeanTorque))
        return value
