'''_1705.py

XmlBearingTypeMapping
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.bearings.bearing_designs.rolling.xml_import import _1703, _1702
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_XML_BEARING_TYPE_MAPPING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling.XmlImport', 'XmlBearingTypeMapping')


__docformat__ = 'restructuredtext en'
__all__ = ('XmlBearingTypeMapping',)


class XmlBearingTypeMapping(_1.APIBase):
    '''XmlBearingTypeMapping

    This is a mastapy class.
    '''

    TYPE = _XML_BEARING_TYPE_MAPPING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'XmlBearingTypeMapping.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def source_name(self) -> 'str':
        '''str: 'SourceName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SourceName

    @property
    def import_all(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ImportAll' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImportAll

    @property
    def target_type(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'TargetType' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.TargetType) if self.wrapped.TargetType else None

    @target_type.setter
    def target_type(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.TargetType = value

    @property
    def number_of_bearings(self) -> 'int':
        '''int: 'NumberOfBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfBearings

    @property
    def number_of_variables(self) -> 'int':
        '''int: 'NumberOfVariables' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfVariables

    @property
    def number_of_unassigned_variables(self) -> 'int':
        '''int: 'NumberOfUnassignedVariables' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfUnassignedVariables

    @property
    def files(self) -> 'List[_1703.BearingImportFile]':
        '''List[BearingImportFile]: 'Files' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Files, constructor.new(_1703.BearingImportFile))
        return value

    @property
    def variables(self) -> 'List[_1702.AbstractXmlVariableAssignment]':
        '''List[AbstractXmlVariableAssignment]: 'Variables' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Variables, constructor.new(_1702.AbstractXmlVariableAssignment))
        return value
