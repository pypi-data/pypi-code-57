'''_785.py

ShaverRedressing
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _786
from mastapy._internal.python_net import python_net_import

_SHAVER_REDRESSING = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShaverRedressing')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaverRedressing',)


T = TypeVar('T', bound='_786.ShavingDynamics')


class ShaverRedressing(_1.APIBase, Generic[T]):
    '''ShaverRedressing

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _SHAVER_REDRESSING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaverRedressing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def redressings(self) -> 'List[T]':
        '''List[T]: 'Redressings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Redressings, constructor.new(T))
        return value

    @property
    def selected_redressings(self) -> 'List[T]':
        '''List[T]: 'SelectedRedressings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SelectedRedressings, constructor.new(T))
        return value
