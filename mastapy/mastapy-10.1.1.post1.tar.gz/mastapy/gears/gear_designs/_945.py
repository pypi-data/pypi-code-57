'''_945.py

GearDesignComponent
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_DESIGN_COMPONENT = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'GearDesignComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('GearDesignComponent',)


class GearDesignComponent(_1.APIBase):
    '''GearDesignComponent

    This is a mastapy class.
    '''

    TYPE = _GEAR_DESIGN_COMPONENT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearDesignComponent.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    def dispose(self):
        ''' 'Dispose' is the original name of this method.'''

        self.wrapped.Dispose()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.dispose()
