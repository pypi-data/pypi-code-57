'''_1887.py

PerLinkExportOptions
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.nodal_analysis.dev_tools_analyses import _207
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PER_LINK_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'PerLinkExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('PerLinkExportOptions',)


class PerLinkExportOptions(_1.APIBase):
    '''PerLinkExportOptions

    This is a mastapy class.
    '''

    TYPE = _PER_LINK_EXPORT_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PerLinkExportOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def type_of_coupling_to_export(self) -> 'overridable.Overridable_RigidCouplingType':
        '''overridable.Overridable_RigidCouplingType: 'TypeOfCouplingToExport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_RigidCouplingType)(self.wrapped.TypeOfCouplingToExport) if self.wrapped.TypeOfCouplingToExport else None

    @type_of_coupling_to_export.setter
    def type_of_coupling_to_export(self, value: 'overridable.Overridable_RigidCouplingType.implicit_type()'):
        wrapper_type = overridable.Overridable_RigidCouplingType.TYPE
        enclosed_type = overridable.Overridable_RigidCouplingType.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.TypeOfCouplingToExport = value
