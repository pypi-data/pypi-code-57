'''_6216.py

HarmonicSelection
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_HARMONIC_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'HarmonicSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicSelection',)


class HarmonicSelection(_1.APIBase):
    '''HarmonicSelection

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def harmonic(self) -> 'int':
        '''int: 'Harmonic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Harmonic

    @property
    def order(self) -> 'float':
        '''float: 'Order' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Order

    @property
    def is_shown(self) -> 'bool':
        '''bool: 'IsShown' is the original name of this property.'''

        return self.wrapped.IsShown

    @is_shown.setter
    def is_shown(self, value: 'bool'):
        self.wrapped.IsShown = bool(value) if value else False
