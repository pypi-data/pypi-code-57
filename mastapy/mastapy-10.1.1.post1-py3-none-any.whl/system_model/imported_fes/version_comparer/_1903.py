'''_1903.py

NodeComparisonResult
'''


from mastapy._internal import constructor
from mastapy.math_utility.measured_vectors import _1250, _1253
from mastapy.utility.units_and_measurements.measurements import _1326, _1283
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_NODE_COMPARISON_RESULT = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs.VersionComparer', 'NodeComparisonResult')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeComparisonResult',)


class NodeComparisonResult(_1.APIBase):
    '''NodeComparisonResult

    This is a mastapy class.
    '''

    TYPE = _NODE_COMPARISON_RESULT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'NodeComparisonResult.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def details(self) -> 'str':
        '''str: 'Details' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Details

    @property
    def linear_change(self) -> 'float':
        '''float: 'LinearChange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LinearChange

    @property
    def angular_change(self) -> 'float':
        '''float: 'AngularChange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngularChange

    @property
    def original_result(self) -> '_1250.NodeResults':
        '''NodeResults: 'OriginalResult' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1250.NodeResults)(self.wrapped.OriginalResult) if self.wrapped.OriginalResult else None

    @property
    def new_result(self) -> '_1250.NodeResults':
        '''NodeResults: 'NewResult' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1250.NodeResults)(self.wrapped.NewResult) if self.wrapped.NewResult else None

    @property
    def displacement_change(self) -> '_1253.VectorWithLinearAndAngularComponents[_1326.LengthVeryShort, _1283.AngleSmall]':
        '''VectorWithLinearAndAngularComponents[LengthVeryShort, AngleSmall]: 'DisplacementChange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1253.VectorWithLinearAndAngularComponents)[_1326.LengthVeryShort, _1283.AngleSmall](self.wrapped.DisplacementChange) if self.wrapped.DisplacementChange else None
