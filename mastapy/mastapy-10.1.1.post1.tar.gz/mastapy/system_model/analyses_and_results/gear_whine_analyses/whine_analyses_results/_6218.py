'''_6218.py

ResultLocationSelectionGroup
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import _6187
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_RESULT_LOCATION_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'ResultLocationSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultLocationSelectionGroup',)


class ResultLocationSelectionGroup(_1.APIBase):
    '''ResultLocationSelectionGroup

    This is a mastapy class.
    '''

    TYPE = _RESULT_LOCATION_SELECTION_GROUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultLocationSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def remove_nodes(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RemoveNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveNodes

    @property
    def response_locations(self) -> 'List[_6187.ResultNodeSelection]':
        '''List[ResultNodeSelection]: 'ResponseLocations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ResponseLocations, constructor.new(_6187.ResultNodeSelection))
        return value
