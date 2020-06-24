'''_1723.py

DesignEntity
'''


from typing import Callable, List

from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.system_model import _1719
from mastapy.utility.model_validation import _1380
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DESIGN_ENTITY = python_net_import('SMT.MastaAPI.SystemModel', 'DesignEntity')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignEntity',)


class DesignEntity(_1.APIBase):
    '''DesignEntity

    This is a mastapy class.
    '''

    TYPE = _DESIGN_ENTITY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignEntity.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def unique_name(self) -> 'str':
        '''str: 'UniqueName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UniqueName

    @property
    def id(self) -> 'str':
        '''str: 'ID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ID

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def icon(self) -> 'Image':
        '''Image: 'Icon' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.Icon)
        return value

    @property
    def small_icon(self) -> 'Image':
        '''Image: 'SmallIcon' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.SmallIcon)
        return value

    @property
    def design_properties(self) -> '_1719.Design':
        '''Design: 'DesignProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1719.Design)(self.wrapped.DesignProperties) if self.wrapped.DesignProperties else None

    @property
    def all_design_entities(self) -> 'List[DesignEntity]':
        '''List[DesignEntity]: 'AllDesignEntities' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllDesignEntities, constructor.new(DesignEntity))
        return value

    @property
    def status(self) -> '_1380.Status':
        '''Status: 'Status' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1380.Status)(self.wrapped.Status) if self.wrapped.Status else None
