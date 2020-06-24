'''_1577.py

LoadedElement
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling import _1636
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_LOADED_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedElement',)


class LoadedElement(_1.APIBase):
    '''LoadedElement

    This is a mastapy class.
    '''

    TYPE = _LOADED_ELEMENT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedElement.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def axial_loading(self) -> 'float':
        '''float: 'AxialLoading' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialLoading

    @property
    def angle(self) -> 'float':
        '''float: 'Angle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Angle

    @property
    def normal_load_inner(self) -> 'float':
        '''float: 'NormalLoadInner' is the original name of this property.'''

        return self.wrapped.NormalLoadInner

    @normal_load_inner.setter
    def normal_load_inner(self, value: 'float'):
        self.wrapped.NormalLoadInner = float(value) if value else 0.0

    @property
    def normal_load_outer(self) -> 'float':
        '''float: 'NormalLoadOuter' is the original name of this property.'''

        return self.wrapped.NormalLoadOuter

    @normal_load_outer.setter
    def normal_load_outer(self, value: 'float'):
        self.wrapped.NormalLoadOuter = float(value) if value else 0.0

    @property
    def race_deflection_outer(self) -> 'float':
        '''float: 'RaceDeflectionOuter' is the original name of this property.'''

        return self.wrapped.RaceDeflectionOuter

    @race_deflection_outer.setter
    def race_deflection_outer(self, value: 'float'):
        self.wrapped.RaceDeflectionOuter = float(value) if value else 0.0

    @property
    def race_deflection_inner(self) -> 'float':
        '''float: 'RaceDeflectionInner' is the original name of this property.'''

        return self.wrapped.RaceDeflectionInner

    @race_deflection_inner.setter
    def race_deflection_inner(self, value: 'float'):
        self.wrapped.RaceDeflectionInner = float(value) if value else 0.0

    @property
    def race_deflection_total(self) -> 'float':
        '''float: 'RaceDeflectionTotal' is the original name of this property.'''

        return self.wrapped.RaceDeflectionTotal

    @race_deflection_total.setter
    def race_deflection_total(self, value: 'float'):
        self.wrapped.RaceDeflectionTotal = float(value) if value else 0.0

    @property
    def race_separation_at_element_radial(self) -> 'float':
        '''float: 'RaceSeparationAtElementRadial' is the original name of this property.'''

        return self.wrapped.RaceSeparationAtElementRadial

    @race_separation_at_element_radial.setter
    def race_separation_at_element_radial(self, value: 'float'):
        self.wrapped.RaceSeparationAtElementRadial = float(value) if value else 0.0

    @property
    def race_separation_at_element_axial(self) -> 'float':
        '''float: 'RaceSeparationAtElementAxial' is the original name of this property.'''

        return self.wrapped.RaceSeparationAtElementAxial

    @race_separation_at_element_axial.setter
    def race_separation_at_element_axial(self, value: 'float'):
        self.wrapped.RaceSeparationAtElementAxial = float(value) if value else 0.0

    @property
    def element_id(self) -> 'str':
        '''str: 'ElementId' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElementId

    @property
    def minimum_lubricating_film_thickness_inner(self) -> 'float':
        '''float: 'MinimumLubricatingFilmThicknessInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumLubricatingFilmThicknessInner

    @property
    def minimum_lubricating_film_thickness_outer(self) -> 'float':
        '''float: 'MinimumLubricatingFilmThicknessOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumLubricatingFilmThicknessOuter

    @property
    def maximum_normal_stress(self) -> 'float':
        '''float: 'MaximumNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalStress

    @property
    def subsurface_shear_stress_distribution_inner(self) -> 'List[_1636.StressAtPosition]':
        '''List[StressAtPosition]: 'SubsurfaceShearStressDistributionInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SubsurfaceShearStressDistributionInner, constructor.new(_1636.StressAtPosition))
        return value

    @property
    def subsurface_shear_stress_distribution_outer(self) -> 'List[_1636.StressAtPosition]':
        '''List[StressAtPosition]: 'SubsurfaceShearStressDistributionOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SubsurfaceShearStressDistributionOuter, constructor.new(_1636.StressAtPosition))
        return value
