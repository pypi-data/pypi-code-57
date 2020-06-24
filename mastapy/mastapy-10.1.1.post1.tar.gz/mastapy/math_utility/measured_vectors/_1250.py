'''_1250.py

NodeResults
'''


from mastapy.math_utility.measured_vectors import _106
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_NODE_RESULTS = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'NodeResults')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeResults',)


class NodeResults(_1.APIBase):
    '''NodeResults

    This is a mastapy class.
    '''

    TYPE = _NODE_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'NodeResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def node_results_in_local_coordinate_system(self) -> '_106.ForceAndDisplacementResults':
        '''ForceAndDisplacementResults: 'NodeResultsInLocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_106.ForceAndDisplacementResults)(self.wrapped.NodeResultsInLocalCoordinateSystem) if self.wrapped.NodeResultsInLocalCoordinateSystem else None

    @property
    def node_results_in_world_coordinate_system(self) -> '_106.ForceAndDisplacementResults':
        '''ForceAndDisplacementResults: 'NodeResultsInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_106.ForceAndDisplacementResults)(self.wrapped.NodeResultsInWorldCoordinateSystem) if self.wrapped.NodeResultsInWorldCoordinateSystem else None
