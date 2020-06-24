'''_991.py

GearSetFCAImportSetup
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _528
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_SET_FCA_IMPORT_SETUP = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'GearSetFCAImportSetup')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetFCAImportSetup',)


class GearSetFCAImportSetup(_1.APIBase):
    '''GearSetFCAImportSetup

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_FCA_IMPORT_SETUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetFCAImportSetup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def meshes(self) -> 'List[_528.CylindricalGearMeshDesign]':
        '''List[CylindricalGearMeshDesign]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Meshes, constructor.new(_528.CylindricalGearMeshDesign))
        return value
