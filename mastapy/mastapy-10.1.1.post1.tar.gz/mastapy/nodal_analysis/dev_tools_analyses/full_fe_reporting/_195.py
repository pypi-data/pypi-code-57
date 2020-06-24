'''_195.py

MaterialPropertiesReporting
'''


from mastapy._internal import constructor, conversion
from mastapy.fe_tools.enums import _284
from mastapy._internal.implicit import overridable
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MATERIAL_PROPERTIES_REPORTING = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'MaterialPropertiesReporting')


__docformat__ = 'restructuredtext en'
__all__ = ('MaterialPropertiesReporting',)


class MaterialPropertiesReporting(_1.APIBase):
    '''MaterialPropertiesReporting

    This is a mastapy class.
    '''

    TYPE = _MATERIAL_PROPERTIES_REPORTING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MaterialPropertiesReporting.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def id(self) -> 'int':
        '''int: 'ID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ID

    @property
    def class_(self) -> '_284.MaterialPropertyClass':
        '''MaterialPropertyClass: 'Class' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.Class)
        return constructor.new(_284.MaterialPropertyClass)(value) if value else None

    @property
    def density(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Density' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Density) if self.wrapped.Density else None

    @density.setter
    def density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Density = value

    @property
    def modulus_of_elasticity(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ModulusOfElasticity' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ModulusOfElasticity) if self.wrapped.ModulusOfElasticity else None

    @modulus_of_elasticity.setter
    def modulus_of_elasticity(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ModulusOfElasticity = value

    @property
    def modulus_of_elasticity_xyz(self) -> 'str':
        '''str: 'ModulusOfElasticityXYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModulusOfElasticityXYZ

    @property
    def shear_modulus_xyz(self) -> 'str':
        '''str: 'ShearModulusXYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShearModulusXYZ

    @property
    def elastic_stiffness_tensor_lower_triangle(self) -> 'str':
        '''str: 'ElasticStiffnessTensorLowerTriangle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElasticStiffnessTensorLowerTriangle

    @property
    def poissons_ratio(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PoissonsRatio' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PoissonsRatio) if self.wrapped.PoissonsRatio else None

    @poissons_ratio.setter
    def poissons_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PoissonsRatio = value

    @property
    def poissons_ratio_xyz(self) -> 'str':
        '''str: 'PoissonsRatioXYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PoissonsRatioXYZ

    @property
    def thermal_expansion_coefficient(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ThermalExpansionCoefficient' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ThermalExpansionCoefficient) if self.wrapped.ThermalExpansionCoefficient else None

    @thermal_expansion_coefficient.setter
    def thermal_expansion_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ThermalExpansionCoefficient = value

    @property
    def thermal_expansion_coefficient_xyz(self) -> 'str':
        '''str: 'ThermalExpansionCoefficientXYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ThermalExpansionCoefficientXYZ
