'''_1159.py

FitAndTolerance
'''


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.detailed_rigid_connectors.splines import _1150, _1156
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FIT_AND_TOLERANCE = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines.TolerancesAndDeviations', 'FitAndTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('FitAndTolerance',)


class FitAndTolerance(_1.APIBase):
    '''FitAndTolerance

    This is a mastapy class.
    '''

    TYPE = _FIT_AND_TOLERANCE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FitAndTolerance.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def fit_class(self) -> 'enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType':
        '''enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType: 'FitClass' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType)(self.wrapped.FitClass) if self.wrapped.FitClass else None

    @fit_class.setter
    def fit_class(self, value: 'enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.FitClass = value

    @property
    def tolerance_class(self) -> 'enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes':
        '''enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes: 'ToleranceClass' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes)(self.wrapped.ToleranceClass) if self.wrapped.ToleranceClass else None

    @tolerance_class.setter
    def tolerance_class(self, value: 'enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ToleranceClass = value
