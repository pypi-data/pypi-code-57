'''_1944.py

SpecifiedConcentricPartGroupDrawingOrder
'''


from typing import Callable

from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model.part_groups import _1947
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SPECIFIED_CONCENTRIC_PART_GROUP_DRAWING_ORDER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Projections', 'SpecifiedConcentricPartGroupDrawingOrder')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecifiedConcentricPartGroupDrawingOrder',)


class SpecifiedConcentricPartGroupDrawingOrder(_1.APIBase):
    '''SpecifiedConcentricPartGroupDrawingOrder

    This is a mastapy class.
    '''

    TYPE = _SPECIFIED_CONCENTRIC_PART_GROUP_DRAWING_ORDER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecifiedConcentricPartGroupDrawingOrder.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def concentric_group(self) -> 'list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup':
        '''list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup: 'ConcentricGroup' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup)(self.wrapped.ConcentricGroup) if self.wrapped.ConcentricGroup else None

    @concentric_group.setter
    def concentric_group(self, value: 'list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ConcentricPartGroup.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ConcentricGroup = value

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
