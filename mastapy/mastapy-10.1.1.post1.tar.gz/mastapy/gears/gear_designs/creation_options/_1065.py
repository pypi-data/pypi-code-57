'''_1065.py

GearSetCreationOptions
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy.gears.gear_designs import _385
from mastapy._internal.python_net import python_net_import

_GEAR_SET_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.CreationOptions', 'GearSetCreationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCreationOptions',)


T = TypeVar('T', bound='_385.GearSetDesign')


class GearSetCreationOptions(_1.APIBase, Generic[T]):
    '''GearSetCreationOptions

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _GEAR_SET_CREATION_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCreationOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def gear_set_design(self) -> 'T':
        '''T: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None
