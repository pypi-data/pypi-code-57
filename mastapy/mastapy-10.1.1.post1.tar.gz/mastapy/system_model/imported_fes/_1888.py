'''_1888.py

PerNodeExportOptions
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.nodal_analysis.fe_export_utility import _172
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PER_NODE_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'PerNodeExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('PerNodeExportOptions',)


class PerNodeExportOptions(_1.APIBase):
    '''PerNodeExportOptions

    This is a mastapy class.
    '''

    TYPE = _PER_NODE_EXPORT_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PerNodeExportOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def external_id(self) -> 'int':
        '''int: 'ExternalID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExternalID

    @property
    def type_of_result_to_export(self) -> 'overridable.Overridable_BoundaryConditionType':
        '''overridable.Overridable_BoundaryConditionType: 'TypeOfResultToExport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_BoundaryConditionType)(self.wrapped.TypeOfResultToExport) if self.wrapped.TypeOfResultToExport else None

    @type_of_result_to_export.setter
    def type_of_result_to_export(self, value: 'overridable.Overridable_BoundaryConditionType.implicit_type()'):
        wrapper_type = overridable.Overridable_BoundaryConditionType.TYPE
        enclosed_type = overridable.Overridable_BoundaryConditionType.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.TypeOfResultToExport = value
