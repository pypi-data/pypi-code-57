'''_914.py

GearNameMapper
'''


from typing import List

from mastapy.gears.gear_set_pareto_optimiser import _915
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_NAME_MAPPER = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'GearNameMapper')


__docformat__ = 'restructuredtext en'
__all__ = ('GearNameMapper',)


class GearNameMapper(_1.APIBase):
    '''GearNameMapper

    This is a mastapy class.
    '''

    TYPE = _GEAR_NAME_MAPPER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearNameMapper.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_name_pickers(self) -> 'List[_915.GearNamePicker]':
        '''List[GearNamePicker]: 'GearNamePickers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearNamePickers, constructor.new(_915.GearNamePicker))
        return value
