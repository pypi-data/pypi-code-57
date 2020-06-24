'''_215.py

CMSOptions
'''


from mastapy._internal import constructor, conversion
from mastapy.math_utility import _241
from mastapy.nodal_analysis.dev_tools_analyses import _175
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CMS_OPTIONS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'CMSOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('CMSOptions',)


class CMSOptions(_1.APIBase):
    '''CMSOptions

    This is a mastapy class.
    '''

    TYPE = _CMS_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CMSOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def mode_options_description(self) -> 'str':
        '''str: 'ModeOptionsDescription' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModeOptionsDescription

    @property
    def store_condensation_node_displacement_expansion(self) -> 'bool':
        '''bool: 'StoreCondensationNodeDisplacementExpansion' is the original name of this property.'''

        return self.wrapped.StoreCondensationNodeDisplacementExpansion

    @store_condensation_node_displacement_expansion.setter
    def store_condensation_node_displacement_expansion(self, value: 'bool'):
        self.wrapped.StoreCondensationNodeDisplacementExpansion = bool(value) if value else False

    @property
    def precision_when_saving_expansion_vectors(self) -> '_241.DataPrecision':
        '''DataPrecision: 'PrecisionWhenSavingExpansionVectors' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PrecisionWhenSavingExpansionVectors)
        return constructor.new(_241.DataPrecision)(value) if value else None

    @precision_when_saving_expansion_vectors.setter
    def precision_when_saving_expansion_vectors(self, value: '_241.DataPrecision'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PrecisionWhenSavingExpansionVectors = value

    @property
    def calculate_reduced_gravity_load(self) -> 'bool':
        '''bool: 'CalculateReducedGravityLoad' is the original name of this property.'''

        return self.wrapped.CalculateReducedGravityLoad

    @calculate_reduced_gravity_load.setter
    def calculate_reduced_gravity_load(self, value: 'bool'):
        self.wrapped.CalculateReducedGravityLoad = bool(value) if value else False

    @property
    def internal_mode_options(self) -> '_175.EigenvalueOptions':
        '''EigenvalueOptions: 'InternalModeOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_175.EigenvalueOptions)(self.wrapped.InternalModeOptions) if self.wrapped.InternalModeOptions else None
