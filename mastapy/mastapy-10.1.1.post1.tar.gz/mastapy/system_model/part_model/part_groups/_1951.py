'''_1951.py

PartGroup
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1931
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PART_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'PartGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('PartGroup',)


class PartGroup(_1.APIBase):
    '''PartGroup

    This is a mastapy class.
    '''

    TYPE = _PART_GROUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def parts(self) -> 'List[_1931.Part]':
        '''List[Part]: 'Parts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Parts, constructor.new(_1931.Part))
        return value
