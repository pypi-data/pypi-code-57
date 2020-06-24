'''_200.py

ElementPropertiesBase
'''


from mastapy._internal import constructor, conversion
from mastapy.fe_tools.enums import _210
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_BASE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesBase',)


class ElementPropertiesBase(_1.APIBase):
    '''ElementPropertiesBase

    This is a mastapy class.
    '''

    TYPE = _ELEMENT_PROPERTIES_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementPropertiesBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def id(self) -> 'int':
        '''int: 'ID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ID

    @property
    def class_(self) -> '_210.ElementPropertyClass':
        '''ElementPropertyClass: 'Class' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.Class)
        return constructor.new(_210.ElementPropertyClass)(value) if value else None
