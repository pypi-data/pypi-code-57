'''_6186.py

ResultLocationSelectionGroups
'''


from typing import Callable, List

from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import _6218
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_RESULT_LOCATION_SELECTION_GROUPS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'ResultLocationSelectionGroups')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultLocationSelectionGroups',)


class ResultLocationSelectionGroups(_1.APIBase):
    '''ResultLocationSelectionGroups

    This is a mastapy class.
    '''

    TYPE = _RESULT_LOCATION_SELECTION_GROUPS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultLocationSelectionGroups.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def select_result_location_group(self) -> 'list_with_selected_item.ListWithSelectedItem_ResultLocationSelectionGroup':
        '''list_with_selected_item.ListWithSelectedItem_ResultLocationSelectionGroup: 'SelectResultLocationGroup' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ResultLocationSelectionGroup)(self.wrapped.SelectResultLocationGroup) if self.wrapped.SelectResultLocationGroup else None

    @select_result_location_group.setter
    def select_result_location_group(self, value: 'list_with_selected_item.ListWithSelectedItem_ResultLocationSelectionGroup.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ResultLocationSelectionGroup.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ResultLocationSelectionGroup.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectResultLocationGroup = value

    @property
    def view_groups(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ViewGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ViewGroups

    @property
    def add_new_group(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddNewGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddNewGroup

    @property
    def display_location_selection(self) -> 'ResultLocationSelectionGroups.DisplayLocationSelectionOption':
        '''DisplayLocationSelectionOption: 'DisplayLocationSelection' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.DisplayLocationSelection)
        return constructor.new(ResultLocationSelectionGroups.DisplayLocationSelectionOption)(value) if value else None

    @display_location_selection.setter
    def display_location_selection(self, value: 'ResultLocationSelectionGroups.DisplayLocationSelectionOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DisplayLocationSelection = value

    @property
    def remove_groups(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RemoveGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveGroups

    @property
    def selected_result_location_group(self) -> '_6218.ResultLocationSelectionGroup':
        '''ResultLocationSelectionGroup: 'SelectedResultLocationGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6218.ResultLocationSelectionGroup)(self.wrapped.SelectedResultLocationGroup) if self.wrapped.SelectedResultLocationGroup else None

    @property
    def result_location_groups(self) -> 'List[_6218.ResultLocationSelectionGroup]':
        '''List[ResultLocationSelectionGroup]: 'ResultLocationGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ResultLocationGroups, constructor.new(_6218.ResultLocationSelectionGroup))
        return value
