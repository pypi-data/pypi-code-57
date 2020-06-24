'''_1948.py

ConcentricPartGroupParallelToThis
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model.part_groups import _1946, _1947, _1950
from mastapy._internal.cast_exception import CastException
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CONCENTRIC_PART_GROUP_PARALLEL_TO_THIS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'ConcentricPartGroupParallelToThis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConcentricPartGroupParallelToThis',)


class ConcentricPartGroupParallelToThis(_1.APIBase):
    '''ConcentricPartGroupParallelToThis

    This is a mastapy class.
    '''

    TYPE = _CONCENTRIC_PART_GROUP_PARALLEL_TO_THIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConcentricPartGroupParallelToThis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def centre_distance(self) -> 'float':
        '''float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CentreDistance

    @property
    def parallel_group(self) -> '_1946.ConcentricOrParallelPartGroup':
        '''ConcentricOrParallelPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1946.ConcentricOrParallelPartGroup)(self.wrapped.ParallelGroup) if self.wrapped.ParallelGroup else None

    @property
    def parallel_group_of_type_concentric_part_group(self) -> '_1947.ConcentricPartGroup':
        '''ConcentricPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ParallelGroup.__class__.__qualname__ != 'ConcentricPartGroup':
            raise CastException('Failed to cast parallel_group to ConcentricPartGroup. Expected: {}.'.format(self.wrapped.ParallelGroup.__class__.__qualname__))

        return constructor.new(_1947.ConcentricPartGroup)(self.wrapped.ParallelGroup) if self.wrapped.ParallelGroup else None

    @property
    def parallel_group_of_type_parallel_part_group(self) -> '_1950.ParallelPartGroup':
        '''ParallelPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ParallelGroup.__class__.__qualname__ != 'ParallelPartGroup':
            raise CastException('Failed to cast parallel_group to ParallelPartGroup. Expected: {}.'.format(self.wrapped.ParallelGroup.__class__.__qualname__))

        return constructor.new(_1950.ParallelPartGroup)(self.wrapped.ParallelGroup) if self.wrapped.ParallelGroup else None
