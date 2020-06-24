'''_5247.py

ComponentStaticLoadCaseGroup
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5249
from mastapy.system_model.part_model import _1989
from mastapy.system_model.analyses_and_results.static_loads import _6071
from mastapy._internal.python_net import python_net_import

_COMPONENT_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'ComponentStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentStaticLoadCaseGroup',)


TReal = TypeVar('TReal', bound='_1989.Component')
TComponentStaticLoad = TypeVar('TComponentStaticLoad', bound='_6071.ComponentLoadCase')


class ComponentStaticLoadCaseGroup(_5249.DesignEntityStaticLoadCaseGroup, Generic[TReal, TComponentStaticLoad]):
    '''ComponentStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TReal
        TComponentStaticLoad
    '''

    TYPE = _COMPONENT_STATIC_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component(self) -> 'TReal':
        '''TReal: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TReal)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_load_cases(self) -> 'List[TComponentStaticLoad]':
        '''List[TComponentStaticLoad]: 'ComponentLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentLoadCases, constructor.new(TComponentStaticLoad))
        return value
