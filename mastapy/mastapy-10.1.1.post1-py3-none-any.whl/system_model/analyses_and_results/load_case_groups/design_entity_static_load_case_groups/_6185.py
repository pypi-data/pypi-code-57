'''_6185.py

GearSetStaticLoadCaseGroup
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _6182, _6183, _6184
from mastapy.system_model.part_model.gears import _1991, _1989
from mastapy.system_model.analyses_and_results.static_loads import _2353, _2306, _2354
from mastapy.system_model.connections_and_sockets.gears import _1802
from mastapy._internal.python_net import python_net_import

_GEAR_SET_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'GearSetStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetStaticLoadCaseGroup',)


TGearSet = TypeVar('TGearSet', bound='_1991.GearSet')
TGear = TypeVar('TGear', bound='_1989.Gear')
TGearStaticLoad = TypeVar('TGearStaticLoad', bound='_2353.GearLoadCase')
TGearMesh = TypeVar('TGearMesh', bound='_1802.GearMesh')
TGearMeshStaticLoad = TypeVar('TGearMeshStaticLoad', bound='_2306.GearMeshLoadCase')
TGearSetStaticLoad = TypeVar('TGearSetStaticLoad', bound='_2354.GearSetLoadCase')


class GearSetStaticLoadCaseGroup(_6184.DesignEntityStaticLoadCaseGroup, Generic[TGearSet, TGear, TGearStaticLoad, TGearMesh, TGearMeshStaticLoad, TGearSetStaticLoad]):
    '''GearSetStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TGearSet
        TGear
        TGearStaticLoad
        TGearMesh
        TGearMeshStaticLoad
        TGearSetStaticLoad
    '''

    TYPE = _GEAR_SET_STATIC_LOAD_CASE_GROUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_set(self) -> 'TGearSet':
        '''TGearSet: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TGearSet)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gears_load_cases(self) -> 'List[_6182.ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]':
        '''List[ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]: 'GearsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsLoadCases, constructor.new(_6182.ComponentStaticLoadCaseGroup)[TGear, TGearStaticLoad])
        return value

    @property
    def meshes_load_cases(self) -> 'List[_6183.ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]':
        '''List[ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]: 'MeshesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesLoadCases, constructor.new(_6183.ConnectionStaticLoadCaseGroup)[TGearMesh, TGearMeshStaticLoad])
        return value

    @property
    def gear_set_load_cases(self) -> 'List[TGearSetStaticLoad]':
        '''List[TGearSetStaticLoad]: 'GearSetLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSetLoadCases, constructor.new(TGearSetStaticLoad))
        return value
