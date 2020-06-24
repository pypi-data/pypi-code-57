'''_397.py

AbstractGearSetAnalysis
'''


from mastapy._internal import constructor
from mastapy.utility.model_validation import _1280
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ABSTRACT_GEAR_SET_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Analysis', 'AbstractGearSetAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractGearSetAnalysis',)


class AbstractGearSetAnalysis(_1.APIBase):
    '''AbstractGearSetAnalysis

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_GEAR_SET_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractGearSetAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def status(self) -> '_1280.Status':
        '''Status: 'Status' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1280.Status)(self.wrapped.Status) if self.wrapped.Status else None
