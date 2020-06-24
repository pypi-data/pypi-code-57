'''_2061.py

ConceptGearSet
'''


from typing import List

from mastapy.gears.gear_designs.concept import _912
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2060, _2071
from mastapy.system_model.connections_and_sockets.gears import _1866
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSet',)


class ConceptGearSet(_2071.GearSet):
    '''ConceptGearSet

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSet.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def active_gear_set_design(self) -> '_912.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_912.ConceptGearSetDesign)(self.wrapped.ActiveGearSetDesign) if self.wrapped.ActiveGearSetDesign else None

    @property
    def concept_gear_set_design(self) -> '_912.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'ConceptGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_912.ConceptGearSetDesign)(self.wrapped.ConceptGearSetDesign) if self.wrapped.ConceptGearSetDesign else None

    @property
    def concept_gears(self) -> 'List[_2060.ConceptGear]':
        '''List[ConceptGear]: 'ConceptGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGears, constructor.new(_2060.ConceptGear))
        return value

    @property
    def concept_meshes(self) -> 'List[_1866.ConceptGearMesh]':
        '''List[ConceptGearMesh]: 'ConceptMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshes, constructor.new(_1866.ConceptGearMesh))
        return value
