'''_1442.py

TextFileDelimiterOptions
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_TEXT_FILE_DELIMITER_OPTIONS = python_net_import('SMT.MastaAPI.Utility.FileAccessHelpers', 'TextFileDelimiterOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('TextFileDelimiterOptions',)


class TextFileDelimiterOptions(_1.APIBase):
    '''TextFileDelimiterOptions

    This is a mastapy class.
    '''

    TYPE = _TEXT_FILE_DELIMITER_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TextFileDelimiterOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def use_comma(self) -> 'bool':
        '''bool: 'UseComma' is the original name of this property.'''

        return self.wrapped.UseComma

    @use_comma.setter
    def use_comma(self, value: 'bool'):
        self.wrapped.UseComma = bool(value) if value else False

    @property
    def use_tab(self) -> 'bool':
        '''bool: 'UseTab' is the original name of this property.'''

        return self.wrapped.UseTab

    @use_tab.setter
    def use_tab(self, value: 'bool'):
        self.wrapped.UseTab = bool(value) if value else False

    @property
    def use_space(self) -> 'bool':
        '''bool: 'UseSpace' is the original name of this property.'''

        return self.wrapped.UseSpace

    @use_space.setter
    def use_space(self, value: 'bool'):
        self.wrapped.UseSpace = bool(value) if value else False

    @property
    def use_semi_colon(self) -> 'bool':
        '''bool: 'UseSemiColon' is the original name of this property.'''

        return self.wrapped.UseSemiColon

    @use_semi_colon.setter
    def use_semi_colon(self, value: 'bool'):
        self.wrapped.UseSemiColon = bool(value) if value else False

    @property
    def other(self) -> 'str':
        '''str: 'Other' is the original name of this property.'''

        return self.wrapped.Other

    @other.setter
    def other(self, value: 'str'):
        self.wrapped.Other = str(value) if value else None

    @property
    def treat_consecutive_delimiters_as_one(self) -> 'bool':
        '''bool: 'TreatConsecutiveDelimitersAsOne' is the original name of this property.'''

        return self.wrapped.TreatConsecutiveDelimitersAsOne

    @treat_consecutive_delimiters_as_one.setter
    def treat_consecutive_delimiters_as_one(self, value: 'bool'):
        self.wrapped.TreatConsecutiveDelimitersAsOne = bool(value) if value else False
