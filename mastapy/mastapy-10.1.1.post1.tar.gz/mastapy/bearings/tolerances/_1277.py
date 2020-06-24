'''_1277.py

SupportTolerance
'''


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.bearings.tolerances import _1388, _1501, _1493
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_SUPPORT_TOLERANCE = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'SupportTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('SupportTolerance',)


class SupportTolerance(_1493.InterferenceTolerance):
    '''SupportTolerance

    This is a mastapy class.
    '''

    TYPE = _SUPPORT_TOLERANCE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SupportTolerance.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def tolerance_band_designation(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ITDesignation':
        '''enum_with_selected_value.EnumWithSelectedValue_ITDesignation: 'ToleranceBandDesignation' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ITDesignation)(self.wrapped.ToleranceBandDesignation) if self.wrapped.ToleranceBandDesignation else None

    @tolerance_band_designation.setter
    def tolerance_band_designation(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ITDesignation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ITDesignation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ITDesignation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ToleranceBandDesignation = value

    @property
    def tolerance_deviation_class(self) -> 'enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation':
        '''enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation: 'ToleranceDeviationClass' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation)(self.wrapped.ToleranceDeviationClass) if self.wrapped.ToleranceDeviationClass else None

    @tolerance_deviation_class.setter
    def tolerance_deviation_class(self, value: 'enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SupportToleranceLocationDesignation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ToleranceDeviationClass = value
