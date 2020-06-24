'''_941.py

ReasonsForInvalidDesigns
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_REASONS_FOR_INVALID_DESIGNS = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ReasonsForInvalidDesigns')


__docformat__ = 'restructuredtext en'
__all__ = ('ReasonsForInvalidDesigns',)


class ReasonsForInvalidDesigns(_1.APIBase):
    '''ReasonsForInvalidDesigns

    This is a mastapy class.
    '''

    TYPE = _REASONS_FOR_INVALID_DESIGNS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ReasonsForInvalidDesigns.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def status_message(self) -> 'str':
        '''str: 'StatusMessage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StatusMessage

    @property
    def number_of_invalidated_designs(self) -> 'int':
        '''int: 'NumberOfInvalidatedDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfInvalidatedDesigns
