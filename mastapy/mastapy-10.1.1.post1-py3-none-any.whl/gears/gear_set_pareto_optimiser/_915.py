'''_915.py

GearNamePicker
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_NAME_PICKER = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'GearNamePicker')


__docformat__ = 'restructuredtext en'
__all__ = ('GearNamePicker',)


class GearNamePicker(_1.APIBase):
    '''GearNamePicker

    This is a mastapy class.
    '''

    TYPE = _GEAR_NAME_PICKER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearNamePicker.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def names_detected_from_file(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'NamesDetectedFromFile' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.NamesDetectedFromFile) if self.wrapped.NamesDetectedFromFile else None

    @names_detected_from_file.setter
    def names_detected_from_file(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.NamesDetectedFromFile = value

    @property
    def gear(self) -> 'str':
        '''str: 'Gear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Gear
