'''_336.py

AbstractGearAnalysis
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ABSTRACT_GEAR_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Analysis', 'AbstractGearAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractGearAnalysis',)


class AbstractGearAnalysis(_1.APIBase):
    '''AbstractGearAnalysis

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_GEAR_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractGearAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def planet_index(self) -> 'int':
        '''int: 'PlanetIndex' is the original name of this property.'''

        return self.wrapped.PlanetIndex

    @planet_index.setter
    def planet_index(self, value: 'int'):
        self.wrapped.PlanetIndex = int(value) if value else 0

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def name_with_gear_set_name(self) -> 'str':
        '''str: 'NameWithGearSetName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NameWithGearSetName
