'''_71.py

AbstractNodalMatrix
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ABSTRACT_NODAL_MATRIX = python_net_import('SMT.MastaAPI.NodalAnalysis', 'AbstractNodalMatrix')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractNodalMatrix',)


class AbstractNodalMatrix(_1.APIBase):
    '''AbstractNodalMatrix

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_NODAL_MATRIX
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractNodalMatrix.TYPE'):
        super().__init__(instance_to_wrap)
