'''_110.py

NodalMatrixRow
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_NODAL_MATRIX_ROW = python_net_import('SMT.MastaAPI.NodalAnalysis', 'NodalMatrixRow')


__docformat__ = 'restructuredtext en'
__all__ = ('NodalMatrixRow',)


class NodalMatrixRow(_1.APIBase):
    '''NodalMatrixRow

    This is a mastapy class.
    '''

    TYPE = _NODAL_MATRIX_ROW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'NodalMatrixRow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def node_index(self) -> 'int':
        '''int: 'NodeIndex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NodeIndex

    @property
    def degree_of_freedom(self) -> 'int':
        '''int: 'DegreeOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DegreeOfFreedom

    @property
    def comma_separated_values(self) -> 'str':
        '''str: 'CommaSeparatedValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CommaSeparatedValues
