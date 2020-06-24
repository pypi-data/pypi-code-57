'''_633.py

MicroGeometryInputs
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy.gears.manufacturing.cylindrical import _636
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_INPUTS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'MicroGeometryInputs')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryInputs',)


T = TypeVar('T', bound='_636.ModificationSegment')


class MicroGeometryInputs(_1.APIBase, Generic[T]):
    '''MicroGeometryInputs

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _MICRO_GEOMETRY_INPUTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MicroGeometryInputs.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def modification_at_starting_point(self) -> 'float':
        '''float: 'ModificationAtStartingPoint' is the original name of this property.'''

        return self.wrapped.ModificationAtStartingPoint

    @modification_at_starting_point.setter
    def modification_at_starting_point(self, value: 'float'):
        self.wrapped.ModificationAtStartingPoint = float(value) if value else 0.0

    @property
    def micro_geometry_segments(self) -> 'List[T]':
        '''List[T]: 'MicroGeometrySegments' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MicroGeometrySegments, constructor.new(T))
        return value
