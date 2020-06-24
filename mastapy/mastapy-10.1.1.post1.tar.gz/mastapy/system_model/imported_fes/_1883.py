'''_1883.py

NodeBoundaryConditionStaticAnalysis
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes import _1849, _1848
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_NODE_BOUNDARY_CONDITION_STATIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'NodeBoundaryConditionStaticAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeBoundaryConditionStaticAnalysis',)


class NodeBoundaryConditionStaticAnalysis(_1.APIBase):
    '''NodeBoundaryConditionStaticAnalysis

    This is a mastapy class.
    '''

    TYPE = _NODE_BOUNDARY_CONDITION_STATIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'NodeBoundaryConditionStaticAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def ground_all_degrees_of_freedom(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'GroundAllDegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GroundAllDegreesOfFreedom

    @property
    def boundary_conditions_linear(self) -> 'List[_1849.DegreeOfFreedomBoundaryConditionLinear]':
        '''List[DegreeOfFreedomBoundaryConditionLinear]: 'BoundaryConditionsLinear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsLinear, constructor.new(_1849.DegreeOfFreedomBoundaryConditionLinear))
        return value

    @property
    def boundary_conditions_angular(self) -> 'List[_1848.DegreeOfFreedomBoundaryConditionAngular]':
        '''List[DegreeOfFreedomBoundaryConditionAngular]: 'BoundaryConditionsAngular' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsAngular, constructor.new(_1848.DegreeOfFreedomBoundaryConditionAngular))
        return value
