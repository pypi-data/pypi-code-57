'''_46.py

ShaftSectionDamageResults
'''


from mastapy._internal import constructor
from mastapy.shafts import _45
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_SECTION_DAMAGE_RESULTS = python_net_import('SMT.MastaAPI.Shafts', 'ShaftSectionDamageResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSectionDamageResults',)


class ShaftSectionDamageResults(_1.APIBase):
    '''ShaftSectionDamageResults

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SECTION_DAMAGE_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSectionDamageResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def left_end(self) -> '_45.ShaftSectionEndDamageResults':
        '''ShaftSectionEndDamageResults: 'LeftEnd' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_45.ShaftSectionEndDamageResults)(self.wrapped.LeftEnd) if self.wrapped.LeftEnd else None

    @property
    def right_end(self) -> '_45.ShaftSectionEndDamageResults':
        '''ShaftSectionEndDamageResults: 'RightEnd' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_45.ShaftSectionEndDamageResults)(self.wrapped.RightEnd) if self.wrapped.RightEnd else None
