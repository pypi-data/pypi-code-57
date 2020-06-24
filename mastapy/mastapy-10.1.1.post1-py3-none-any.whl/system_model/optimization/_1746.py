'''_1746.py

CylindricalGearSetOptimizer
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.optimization import _1747
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_OPTIMIZER = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'CylindricalGearSetOptimizer')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetOptimizer',)


class CylindricalGearSetOptimizer(_1.APIBase):
    '''CylindricalGearSetOptimizer

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_OPTIMIZER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetOptimizer.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def create_new_design(self) -> 'bool':
        '''bool: 'CreateNewDesign' is the original name of this property.'''

        return self.wrapped.CreateNewDesign

    @create_new_design.setter
    def create_new_design(self, value: 'bool'):
        self.wrapped.CreateNewDesign = bool(value) if value else False

    @property
    def new_design_name(self) -> 'str':
        '''str: 'NewDesignName' is the original name of this property.'''

        return self.wrapped.NewDesignName

    @new_design_name.setter
    def new_design_name(self, value: 'str'):
        self.wrapped.NewDesignName = str(value) if value else None

    @property
    def constraints(self) -> 'List[_1747.MeasuredAndFactorViewModel]':
        '''List[MeasuredAndFactorViewModel]: 'Constraints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Constraints, constructor.new(_1747.MeasuredAndFactorViewModel))
        return value
