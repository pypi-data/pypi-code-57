'''_934.py

GearSetFEModel
'''


from typing import Callable, List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _1367
from mastapy.gears.fe_model import _932, _931
from mastapy import _6501
from mastapy.gears.analysis import _962
from mastapy._internal.python_net import python_net_import

_GEAR_SET_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel', 'GearSetFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetFEModel',)


class GearSetFEModel(_962.GearSetImplementationDetail):
    '''GearSetFEModel

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_FE_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetFEModel.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_coupled_teeth_either_side(self) -> 'int':
        '''int: 'NumberOfCoupledTeethEitherSide' is the original name of this property.'''

        return self.wrapped.NumberOfCoupledTeethEitherSide

    @number_of_coupled_teeth_either_side.setter
    def number_of_coupled_teeth_either_side(self, value: 'int'):
        self.wrapped.NumberOfCoupledTeethEitherSide = int(value) if value else 0

    @property
    def element_order(self) -> '_1367.ElementOrder':
        '''ElementOrder: 'ElementOrder' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ElementOrder)
        return constructor.new(_1367.ElementOrder)(value) if value else None

    @element_order.setter
    def element_order(self, value: '_1367.ElementOrder'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ElementOrder = value

    @property
    def generate_stiffness_from_fe(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'GenerateStiffnessFromFE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GenerateStiffnessFromFE

    @property
    def generate_stress_influence_coefficients_from_fe(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'GenerateStressInfluenceCoefficientsFromFE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GenerateStressInfluenceCoefficientsFromFE

    @property
    def comment(self) -> 'str':
        '''str: 'Comment' is the original name of this property.'''

        return self.wrapped.Comment

    @comment.setter
    def comment(self, value: 'str'):
        self.wrapped.Comment = str(value) if value else None

    @property
    def mesh_fe_models(self) -> 'List[_932.GearMeshFEModel]':
        '''List[GearMeshFEModel]: 'MeshFEModels' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshFEModels, constructor.new(_932.GearMeshFEModel))
        return value

    @property
    def gear_fe_models(self) -> 'List[_931.GearFEModel]':
        '''List[GearFEModel]: 'GearFEModels' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearFEModels, constructor.new(_931.GearFEModel))
        return value

    def calculate_stiffness_from_fe(self):
        ''' 'CalculateStiffnessFromFE' is the original name of this method.'''

        self.wrapped.CalculateStiffnessFromFE()

    def calculate_stiffness_from_fe_with_progress(self, progress: '_6501.TaskProgress'):
        ''' 'CalculateStiffnessFromFE' is the original name of this method.

        Args:
            progress (mastapy.TaskProgress)
        '''

        self.wrapped.CalculateStiffnessFromFE(progress.wrapped if progress else None)
