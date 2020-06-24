'''_1102.py

GearSetFEModel
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.fe_model import _1116, _1115
from mastapy import _312
from mastapy.gears.analysis import _747
from mastapy._internal.python_net import python_net_import

_GEAR_SET_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel', 'GearSetFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetFEModel',)


class GearSetFEModel(_747.GearSetImplementationDetail):
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
    def mesh_fe_models(self) -> 'List[_1116.GearMeshFEModel]':
        '''List[GearMeshFEModel]: 'MeshFEModels' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshFEModels, constructor.new(_1116.GearMeshFEModel))
        return value

    @property
    def gear_fe_models(self) -> 'List[_1115.GearFEModel]':
        '''List[GearFEModel]: 'GearFEModels' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearFEModels, constructor.new(_1115.GearFEModel))
        return value

    def calculate_stiffness_from_fe(self):
        ''' 'CalculateStiffnessFromFE' is the original name of this method.'''

        self.wrapped.CalculateStiffnessFromFE()

    def calculate_stiffness_from_fe_with_progress(self, progress: '_312.TaskProgress'):
        ''' 'CalculateStiffnessFromFE' is the original name of this method.

        Args:
            progress (mastapy.TaskProgress)
        '''

        self.wrapped.CalculateStiffnessFromFE(progress.wrapped if progress else None)
