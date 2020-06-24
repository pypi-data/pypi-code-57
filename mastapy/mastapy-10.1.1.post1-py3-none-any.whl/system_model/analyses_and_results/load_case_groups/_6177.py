'''_6177.py

LoadCaseGroupHistograms
'''


from typing import Callable

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model import _1934
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_LOAD_CASE_GROUP_HISTOGRAMS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'LoadCaseGroupHistograms')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCaseGroupHistograms',)


class LoadCaseGroupHistograms(_1.APIBase):
    '''LoadCaseGroupHistograms

    This is a mastapy class.
    '''

    TYPE = _LOAD_CASE_GROUP_HISTOGRAMS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadCaseGroupHistograms.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_bins(self) -> 'int':
        '''int: 'NumberOfBins' is the original name of this property.'''

        return self.wrapped.NumberOfBins

    @number_of_bins.setter
    def number_of_bins(self, value: 'int'):
        self.wrapped.NumberOfBins = int(value) if value else 0

    @property
    def run_power_flow(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RunPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RunPowerFlow

    @property
    def y_axis_variable(self) -> 'LoadCaseGroupHistograms.RevolutionsOrDuration':
        '''RevolutionsOrDuration: 'YAxisVariable' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.YAxisVariable)
        return constructor.new(LoadCaseGroupHistograms.RevolutionsOrDuration)(value) if value else None

    @y_axis_variable.setter
    def y_axis_variable(self, value: 'LoadCaseGroupHistograms.RevolutionsOrDuration'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.YAxisVariable = value

    @property
    def power_load(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        '''list_with_selected_item.ListWithSelectedItem_PowerLoad: 'PowerLoad' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_PowerLoad)(self.wrapped.PowerLoad) if self.wrapped.PowerLoad else None

    @power_load.setter
    def power_load(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.PowerLoad = value
