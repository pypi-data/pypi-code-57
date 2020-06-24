'''_1749.py

OptimizationStep
'''


from mastapy._internal import constructor, conversion
from mastapy.system_model.optimization import _1748
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_STEP = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'OptimizationStep')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationStep',)


class OptimizationStep(_1.APIBase):
    '''OptimizationStep

    This is a mastapy class.
    '''

    TYPE = _OPTIMIZATION_STEP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptimizationStep.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def target_edge_stress_factor(self) -> 'float':
        '''float: 'TargetEdgeStressFactor' is the original name of this property.'''

        return self.wrapped.TargetEdgeStressFactor

    @target_edge_stress_factor.setter
    def target_edge_stress_factor(self, value: 'float'):
        self.wrapped.TargetEdgeStressFactor = float(value) if value else 0.0

    @property
    def tolerance(self) -> 'float':
        '''float: 'Tolerance' is the original name of this property.'''

        return self.wrapped.Tolerance

    @tolerance.setter
    def tolerance(self, value: 'float'):
        self.wrapped.Tolerance = float(value) if value else 0.0

    @property
    def optimisation_target(self) -> '_1748.MicroGeometryOptimisationTarget':
        '''MicroGeometryOptimisationTarget: 'OptimisationTarget' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OptimisationTarget)
        return constructor.new(_1748.MicroGeometryOptimisationTarget)(value) if value else None

    @optimisation_target.setter
    def optimisation_target(self, value: '_1748.MicroGeometryOptimisationTarget'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OptimisationTarget = value
